"""
HW3 家庭版：拟合 Scaling Law 并做外推预测
==========================================
零依赖（仅 numpy），纯 CPU，秒级跑完。

对应清华《高级机器学习》W2+W4，也是理解唐杰「规模化正确性」的地基：
  你只有先能**拟合出曲线**，才有资格讨论「这条曲线是不是在骗人」。

本脚本做四件事：
  1. 用 Chinchilla 形式 L(N,D) = E + A/N^α + B/D^β 拟合
  2. 用 **留一交叉验证** 检验外推能力（不是只看拟合优度！）
  3. 预测 1T 参数模型的 loss，并给出**预测区间**
  4. 反推 compute-optimal 的参数量↔数据量配比

★ 核心教训（写在最前面）：
  「拟合得好」和「外推得准」是两件事。
  R²=0.999 的曲线，外推到 10× 规模可能错 0.3 个 loss。
  所以本脚本把 **外推误差** 作为主指标，R² 只作参考。
  这也正是唐杰「规模化正确性」的起点：**小规模结论必须证明能外推，否则无效。**
"""

import itertools
import sys
import numpy as np

# ─────────────────────────────────────────────────────────────
# 一、"观测数据"
# ─────────────────────────────────────────────────────────────
# ★ 踩坑记录（本轮实测，非常值得记住）：
#   首版数据里每个点都取 D/N = 20（固定配比），结果拟合出 β=0.49 > α=0.26，
#   compute-optimal 直接跑到边界，算出 tokens/param = 0.0 —— 完全是垃圾。
#   真因：**N 和 D 完全共线时，α 和 β 不可识别**，模型可以随便分配"功劳"。
#   这正是唐杰六维里「数据」那一维的失效形态：**不是数据不够多，是数据没有变化**。
#   修法：让 D/N 在 10~40 之间变化，把 N 和 D 解耦。
#
#   本版更进一步：用**已知真参数**生成数据，再看能不能反向恢复出来。
#   这才是可验证的实验设计 —— 你连自己造的数据都恢复不了，凭什么相信真实拟合？
TRUE_PARAMS = dict(E=1.69, A=406.4, B=410.7, alpha=0.34, beta=0.28)  # Chinchilla 量级
NOISE = 0.008


def _make_observed():
    pts = [
        (1.0e8, 2.0e9),    # D/N = 20
        (3.0e8, 3.0e9),    # D/N = 10
        (1.0e9, 2.0e10),   # D/N = 20
        (3.0e9, 3.0e10),   # D/N = 10
        (7.0e9, 2.8e11),   # D/N = 40
        (1.3e10, 1.3e11),  # D/N = 10
        (7.0e10, 1.4e12),  # D/N = 20
    ]
    rng = np.random.default_rng(42)
    out = []
    for n_, d_ in pts:
        l_ = float(chinchilla_loss(n_, d_, **TRUE_PARAMS))
        l_ += float(rng.normal(0, NOISE))
        out.append((n_, d_, round(l_, 4)))
    return out


def chinchilla_loss(N, D, E, A, B, alpha, beta):
    """Chinchilla 形式：不可约损失 E + 参数项 + 数据项"""
    return E + A / np.power(N, alpha) + B / np.power(D, beta)


OBSERVED = _make_observed()   # 必须在 chinchilla_loss 定义之后才能求值


def fit_scaling_law(rows, init=None, iters=8000, lr=1e-3, verbose=False):
    """
    用 Adam 拟合 5 个参数（E, logA, logB, α, β）。
    为什么要 logA/logB：A、B 量级跨越 10^1~10^9，直接梯度会崩。
    """
    N = np.array([r[0] for r in rows], dtype=float)
    D = np.array([r[1] for r in rows], dtype=float)
    L = np.array([r[2] for r in rows], dtype=float)

    # 参数：E, logA, logB, alpha, beta
    p = np.array(init if init is not None else [1.5, 6.0, 6.0, 0.30, 0.30])
    m = np.zeros_like(p)
    v = np.zeros_like(p)
    b1, b2, eps = 0.9, 0.999, 1e-8

    for t in range(1, iters + 1):
        E, logA, logB, al, be = p
        A, B = np.exp(logA), np.exp(logB)
        pred = E + A * N ** (-al) + B * D ** (-be)
        err = pred - L
        loss = np.mean(err ** 2)

        # 解析梯度
        gE = 2 * np.mean(err)
        gA = 2 * np.mean(err * N ** (-al)) * A          # d/d(logA) = d/dA * A
        gB = 2 * np.mean(err * D ** (-be)) * B
        gal = 2 * np.mean(err * A * N ** (-al) * (-np.log(N)))
        gbe = 2 * np.mean(err * B * D ** (-be) * (-np.log(D)))
        g = np.array([gE, gA, gB, gal, gbe])

        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g ** 2
        mhat = m / (1 - b1 ** t)
        vhat = v / (1 - b2 ** t)
        p = p - lr * mhat / (np.sqrt(vhat) + eps)
        p[0] = max(p[0], 1e-3)     # E > 0
        p[3] = np.clip(p[3], 1e-3, 2.0)
        p[4] = np.clip(p[4], 1e-3, 2.0)
        if verbose and t % 2000 == 0:
            print(f"    iter {t:5d}  rmse={np.sqrt(loss):.6f}  "
                  f"E={p[0]:.3f} A={np.exp(p[1]):.2e} B={np.exp(p[2]):.2e} "
                  f"α={p[3]:.3f} β={p[4]:.3f}")

    E, logA, logB, al, be = p
    return dict(E=E, A=np.exp(logA), B=np.exp(logB), alpha=al, beta=be)


def r2(y, yhat):
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss_res / ss_tot


def main():
    print("=" * 70)
    print("HW3 家庭版 · 拟合 Scaling Law + 留一外推检验")
    print("=" * 70)

    N = np.array([r[0] for r in OBSERVED])
    D = np.array([r[1] for r in OBSERVED])
    L = np.array([r[2] for r in OBSERVED])

    print(f"\n[数据] {len(OBSERVED)} 个观测点，参数量跨度 "
          f"{N.min():.1e} → {N.max():.1e}（{N.max()/N.min():.0f}×）")

    # ---- 1. 全量拟合 ----
    print("\n[1] 全量拟合")
    par = fit_scaling_law(OBSERVED, verbose=True)
    pred = chinchilla_loss(N, D, **par)
    print(f"  E={par['E']:.4f}  A={par['A']:.3e}  B={par['B']:.3e}  "
          f"α={par['alpha']:.4f}  β={par['beta']:.4f}")
    print(f"  R² = {r2(L, pred):.6f}   RMSE = {np.sqrt(np.mean((L-pred)**2)):.6f}")

    # ---- 2. ★ 留一交叉验证：真正的能力检验 ----
    print("\n[2] 留一交叉验证（每次留出最大的一个点，用其余点外推）")
    print("    这才是「规模化正确性」要问的问题：小规模能不能预测大规模？")
    loo_err = []
    for i in range(len(OBSERVED)):
        train = OBSERVED[:i] + OBSERVED[i + 1:]
        pp = fit_scaling_law(train, iters=6000)
        pv = chinchilla_loss(N[i], D[i], **pp)
        e = pv - L[i]
        loo_err.append(e)
        tag = "★外推" if i == len(OBSERVED) - 1 else ""
        print(f"    留出 #{i}  N={N[i]:.1e}  真实={L[i]:.3f}  "
              f"预测={pv:.3f}  误差={e:+.3f}  {tag}")
    loo_err = np.array(loo_err)
    print(f"    → 平均|误差| = {np.abs(loo_err).mean():.4f}  "
          f"最大|误差| = {np.abs(loo_err).max():.4f}")

    # ---- 3. 外推预测 1T ----
    print("\n[3] 外推预测（用全量参数）")
    cases = [
        ("10B  / 200B tok", 1e10, 2e11),
        ("100B / 2T tok", 1e11, 2e12),
        ("1T   / 20T tok", 1e12, 2e13),
    ]
    for name, n_, d_ in cases:
        v = chinchilla_loss(n_, d_, **par)
        # 简单的敏感度区间：α、β 各 ±10% 重新算
        lo = chinchilla_loss(n_, d_, **{**par, 'alpha': par['alpha']*1.1,
                                        'beta': par['beta']*1.1})
        hi = chinchilla_loss(n_, d_, **{**par, 'alpha': par['alpha']*0.9,
                                        'beta': par['beta']*0.9})
        print(f"    {name:16s} 预测 loss ≈ {v:.3f}   "
              f"(指数±10% 敏感区间 {hi:.3f} ~ {lo:.3f})")

    # ---- 4. compute-optimal 配比 ----
    print("\n[4] compute-optimal 配比（固定 1e24 FLOPs ≈ C=6ND）")
    C = 1e24
    best = None
    for n_exp in np.arange(9.0, 13.0, 0.05):
        n_ = 10 ** n_exp
        d_ = C / (6 * n_)
        l_ = chinchilla_loss(n_, d_, **par)
        if best is None or l_ < best[0]:
            best = (l_, n_, d_)
    l_, n_, d_ = best
    print(f"    最优 N = {n_:.3e}   D = {d_:.3e}   预测 loss = {l_:.4f}")
    print(f"    tokens/param = {d_/n_:.1f}  "
          f"（Chinchilla 经验值约 20，这是本数据拟合出来的值）")

    # ---- 5. 验收：能不能恢复出真参数 ----
    print("\n" + "=" * 70)
    print("[验收] 用已知真参数生成数据 → 看拟合能否恢复")
    ok = True
    for k in ["alpha", "beta"]:
        tv, fv = TRUE_PARAMS[k], par[k]
        d_ = abs(tv - fv)
        passed = d_ < 0.06
        ok &= passed
        print(f"  {'✅' if passed else '❌'} {k:6s} 真值={tv:.3f}  "
              f"拟合={fv:.3f}  偏差={d_:.3f}  (阈值 0.06)")
    print(f"\n[验收] 拟合优度 R² = {r2(L, pred):.4f}  —— 但这不是重点")
    print(f"[验收] 外推误差 max = {np.abs(loo_err).max():.4f}  —— 这才是重点")
    print("\n  ★ 三条结论：")
    print("    1. R² 高不代表外推准。小规模曲线必须用留一验证外推误差。")
    print("    2. N 与 D 共线时 α、β 不可识别 —— 这是数据设计的病，不是优化的病。")
    print("    3. 能恢复已知真参数，才有资格说这套拟合方法可信。")
    print("    这就是唐杰 2026「规模化正确性」的最小可执行版本。")
    print("=" * 70)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
