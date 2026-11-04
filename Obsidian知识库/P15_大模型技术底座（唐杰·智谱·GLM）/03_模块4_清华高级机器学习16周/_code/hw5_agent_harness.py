"""
HW5 家庭版：Agent Harness + Self-Judge Loop
============================================
零依赖（仅 Python 标准库），秒级跑完，不调任何外部 API。

对应清华《高级机器学习》W12–W15，也是唐杰 2026-10-31 演讲的直接落地：
  「递归式自我改进能不能跑通，不取决于模型能否生成下一步，
    而是取决于它能否准确判断这一步是不是『进步』。」—— 他称之为「自净化」。

本脚本用一个**可验证的玩具环境**（修复一段有 bug 的代码）演示三件事：
  1. **Harness 结构**：State / Action / Observation / Verifier 四件套
  2. **Self-Judge**：Agent 自己判断"我这一步是变好了还是变坏了"
  3. ★ **反作弊**：self-judge 会被 reward hacking 攻破 —— 脚本内置三种攻击，看它怎么被抓

★ 为什么这个玩具值得做：
  真跑一个 SWE-bench 需要 GPU 和 API key。但看穿这套机制**不需要**。
  Harness 的本质是「用一个可执行的东西当裁判」，玩具环境一样能体现全部结构性缺陷。

跑法：
  python hw5_agent_harness.py
  python hw5_agent_harness.py --verbose
"""

import argparse
import io
import contextlib
import traceback

# ─────────────────────────────────────────────────────────────
# 一、环境：一个有 3 个 bug 的函数 + 一套测试
# ─────────────────────────────────────────────────────────────
# 任务：实现 chunked_mean(xs, k)，把列表按大小 k 切块并返回每块均值。
# 当前实现有 3 个 bug，Agent 需要逐步修好。

BUGGY_SOURCE = '''
def chunked_mean(xs, k):
    out = []
    for i in range(0, len(xs), k):          # BUG-1: k<=0 时不报错，死循环/错切
        chunk = xs[i:i + k]
        out.append(sum(chunk) / len(chunk))  # BUG-2: 空块 ZeroDivisionError
    return out
                                                # BUG-3: 缺少 k 类型/边界校验
'''

TESTS = [
    ("basic",        lambda f: f([1, 2, 3, 4, 5], 2) == [1.5, 3.5, 5.0]),
    ("exact_div",    lambda f: f([2, 4, 6, 8], 2) == [3.0, 7.0]),
    ("k_equals_1",   lambda f: f([1, 2, 3], 1) == [1.0, 2.0, 3.0]),
    ("empty_list",   lambda f: f([], 3) == []),
    ("k_zero",       lambda f: _raises(lambda: f([1, 2], 0), ValueError)),
    ("k_negative",   lambda f: _raises(lambda: f([1, 2], -1), ValueError)),
    ("k_bool",       lambda f: _raises(lambda: f([1, 2], True), TypeError)),
]


def _raises(fn, exc):
    try:
        fn()
        return False
    except exc:
        return True
    except Exception:
        return False


class Sandbox:
    """可验证环境：跑测试、返回通过/失败清单。"""

    def __init__(self):
        self.n_evals = 0

    def load(self, source):
        """把源码编译成可调用对象。语法错误也当成一次失败返回，不抛。"""
        ns = {}
        try:
            exec(compile(source, "<agent_code>", "exec"), ns)
        except SyntaxError as e:
            return None, f"SyntaxError: {e}"
        fn = ns.get("chunked_mean")
        if fn is None:
            return None, "未定义 chunked_mean"
        return fn, None

    def evaluate(self, source):
        """返回 (pass_count, total, failed_names, err)。"""
        self.n_evals += 1
        fn, err = self.load(source)
        if fn is None:
            return 0, len(TESTS), [f"compile:{err}"], err
        passed, failed = 0, []
        for name, t in TESTS:
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    ok = t(fn)
            except Exception:
                ok = False
            if ok:
                passed += 1
            else:
                failed.append(name)
        return passed, len(TESTS), failed, None


# ─────────────────────────────────────────────────────────────
# 二、Self-Judge：判断"这一步是不是进步"
# ─────────────────────────────────────────────────────────────
class SelfJudge:
    """
    最朴素的 judge：比较前后两次测试通过数。
    加分项：区分「真进步」和「假进步」。
    """

    def __init__(self, total):
        self.total = total
        self.history = []

    def score(self, passed, failed, source):
        """
        多目标评分，不只是看通过数 —— 这是防 reward hacking 的第一道墙。
        """
        n = len(failed)
        # ① 主指标：通过数
        s = passed / self.total
        # ② 惩罚 1：源码里出现针对测试名的特判（作弊）
        if "if test" in source or "test_name" in source:
            s -= 0.5
        # ③ 惩罚 2：源码里出现 return True / 裸 raise（绕过）
        if _has_bypass(source):
            s -= 0.3
        # ④ 惩罚 3：代码长度暴涨（暴力堆砌）
        if len(source) > 2.5 * len(BUGGY_SOURCE):
            s -= 0.2
        return max(0.0, min(1.0, s))

    def judge(self, prev, cur):
        """返回 (is_progress, delta, verdict)"""
        if prev is None:
            return True, cur, "首次评估，视为起点"
        d = cur - prev
        if d > 1e-9:
            return True, d, f"✅ 进步 +{d:.3f}"
        if d < -1e-9:
            return True, d, f"⚠️ 退步 {d:.3f}（仍允许继续，用于跳出局部最优）"
        return False, 0.0, "➖ 无变化，应换策略"


def _has_bypass(source):
    """检测明显的作弊写法。"""
    bad = [
        "return True",            # 直接返回 True 骗测试
        "sys.exit(0)",
        "pytest.skip",
        "except:pass",
        "except: pass",
    ]
    stripped = source.replace(" ", "")
    return any(b.replace(" ", "") in stripped for b in bad)


# ─────────────────────────────────────────────────────────────
# 三、Agent：一个"会自己改代码"的循环
# ─────────────────────────────────────────────────────────────
# 每个 candidate 是一次编辑动作（模拟模型生成的补丁）。
# 真实场景里这一步是 LLM 生成，这里用预置补丁序列代替，
# 目的是让 harness 逻辑可被完整验证（而不需要 API key）。
PATCHES = [
    # 第 0 步：原样（基线）
    BUGGY_SOURCE,
    # 第 1 步：只加 k 的边界校验（修 BUG-1/3）
    '''
def chunked_mean(xs, k):
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be int")
    if k <= 0:
        raise ValueError("k must be positive")
    out = []
    for i in range(0, len(xs), k):
        chunk = xs[i:i + k]
        out.append(sum(chunk) / len(chunk))
    return out
''',
    # 第 2 步：再加空块保护（修 BUG-2）—— 完整正确版
    '''
def chunked_mean(xs, k):
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be int")
    if k <= 0:
        raise ValueError("k must be positive")
    out = []
    for i in range(0, len(xs), k):
        chunk = xs[i:i + k]
        if not chunk:
            continue
        out.append(sum(chunk) / len(chunk))
    return out
''',
    # 第 3 步：★ 作弊尝试 —— 直接 return True 骗测试
    '''
def chunked_mean(xs, k):
    return True
''',
    # 第 4 步：★ 作弊尝试 2 —— 针对测试名特判
    '''
def chunked_mean(xs, k):
    if test_name == "basic":
        return [1.5, 3.5, 5.0]
    return [3.0, 7.0]
''',
]


def run(verbose=False):
    env = Sandbox()
    judge = SelfJudge(len(TESTS))
    prev_score = None
    log = []

    print("=" * 70)
    print("HW5 家庭版 · Agent Harness + Self-Judge Loop")
    print("=" * 70)
    print(f"环境：{len(TESTS)} 个测试 · 任务：修好 chunked_mean 的 3 个 bug")
    print(f"初始代码长度 {len(BUGGY_SOURCE)} 字符\n")

    for step, src in enumerate(PATCHES):
        passed, total, failed, err = env.evaluate(src)
        sc = judge.score(passed, failed, src)
        is_prog, delta, verdict = judge.judge(prev_score, sc)

        tag = f"step {step}"
        print(f"[{tag}] 通过 {passed}/{total}  score={sc:.3f}  {verdict}")
        if failed:
            print(f"        失败用例: {failed[:4]}{'...' if len(failed) > 4 else ''}")
        if verbose:
            print("        --- 源码 ---")
            for ln in src.strip().splitlines()[:6]:
                print("        " + ln)
        log.append(dict(step=step, passed=passed, score=sc,
                        failed=failed, progress=is_prog))

        # ★ Self-Judge 的核心用途：如果连续两次没进步，就该换策略 / 停下
        if not is_prog and step > 0:
            print("        ⚠️ judge 判定：本步无进步 → 应触发策略切换")
        prev_score = sc

    # ---------- 汇总 ----------
    print("\n" + "=" * 70)
    print("[反作弊检验]")
    cheat_steps = [r for r in log if r["step"] in (3, 4)]
    caught = [r for r in cheat_steps if r["score"] < 0.5]
    for r in cheat_steps:
        print(f"  step {r['step']}: 通过数={r['passed']}/{len(TESTS)} "
              f"score={r['score']:.3f} → "
              f"{'✅ 已识别为作弊' if r['score'] < 0.5 else '❌ 漏判！'}")
    ok = len(caught) == len(cheat_steps)

    best = max(log, key=lambda r: r["score"])
    print(f"\n[最优] step {best['step']}  score={best['score']:.3f}  "
          f"通过 {best['passed']}/{len(TESTS)}")

    print("\n[结论]")
    print("  1. 「能生成下一步」不值钱，「能判断这步是不是进步」才值钱 —— 这就是自净化。")
    print("  2. 只看通过数一定会被 reward hacking 攻破，必须多目标评分 + 反作弊规则。")
    print("  3. 通关率不是唯一指标：连续 N 步不崩的概率才是产品的真实体验。")
    print("\n  ★ 本轮实测挖到的真问题（比脚本设计更值得记）：")
    print("    标记为 BUG-2 的『空块除零』，在这 7 个测试里**从未被触发** ——")
    print("    因为 range(0, len, k) 在 k>0 时永远不会产出空 chunk。")
    print("    也就是说：**我的测试集有盲区，通过了不代表没问题。**")
    print("    → 这正是唐杰说的「Benchmark 成绩不等于用户体验」的最小案例。")
    print("    → 一个 Bug 要么被真实数据触发，要么它就是不能被验证的假设。")
    print(f"\n[验收] {'✅ 通过：两个作弊样本都被 judge 抓住' if ok else '❌ 未通过：judge 漏判作弊'}")
    print("=" * 70)
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    raise SystemExit(run(a.verbose))
