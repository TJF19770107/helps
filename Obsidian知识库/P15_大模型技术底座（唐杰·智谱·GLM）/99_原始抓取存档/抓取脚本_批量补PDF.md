---
title: 抓取脚本_批量补PDF
aliases: [补PDF, arXiv批量下载, 抓取脚本]
tags: [P15, 工具, 脚本, arXiv, 存档]
created: 2026-11-02
source_type: 我方脚本
status: 未执行（本机境外网络 502）
---

# 抓取脚本 · 批量补 PDF

> ⚠️ **本文件是"备用件"，不是"已完成件"**。
> 2026-11-02 实测：本机到 arXiv 的 urllib 请求返回 `502 Tunnel connection failed`，**PDF 一份都没下**。
> 下面脚本在有梯子（或香港隧道 1081 起来）时可直接跑。

## 一、前置条件

- 有可用代理（本机常见：`127.0.0.1:7897` HTTP 代理；或 ssh 隧道 `1081` socks5）
- 磁盘：40 篇论文约 **300-600MB**（E 盘当前剩 34.2GB，够）

## 二、arXiv 号清单（按模块）

```
# A. 基础架构
1706.03762   Attention Is All You Need
2104.09864   RoPE
2307.08691   FlashAttention-2

# B. 稀疏/高效注意力
2502.11089   Native Sparse Attention
2603.12201   IndexShare (GLM-5.2)
2312.00752   Mamba

# C. 量化
2208.07339   LLM.int8
2211.10438   SmoothQuant
2210.17323   GPTQ
2306.7761    AWQ
2310.18313   FP8-LM

# D. 对齐与 RL
2203.02155   InstructGPT
2305.18290   DPO
2411.15124   Tulu 3 / RLVR
2501.12948   DeepSeek-R1

# E. Agent
2210.03629   ReAct
2310.06770   SWE-bench

# F. GLM / 智谱
2602.15763   GLM-5 技术报告 ★
2210.02414   GLM-130B

# G. Kimi
2507.20534   Kimi K2
2602.02276   Kimi K2.5
2607.24653   Kimi K3 ★

# H. RoboBrain（归 P03）
2502.21257   RoboBrain 1.0
2507.02029   RoboBrain 2.0 ★
2601.14352   RoboBrain 2.5 ★
2505.03673   RoboOS
2503.20752   Reason-RFT
2506.04308   RoboRefer
2512.13660   RoboTracer
2512.23703   Robo-Dopamine
```

> ⚠️ 2602.x / 2603.x / 2607.x / 2512.x 是本轮检索到的 2026 年新号，**未逐条验证可下载性**。

## 三、批量下载脚本（bash）

```bash
#!/usr/bin/env bash
# 用法：PROXY=http://127.0.0.1:7897 bash fetch_arxiv.sh
export PATH="$PATH:/usr/bin:/bin:/c/Windows/System32"
PROXY="${PROXY:-}"
OUT="E:/龙虾AI主控中心/我的AI分身/AI具身智能赛道/outputs/唐杰知识底座/pdfs"
mkdir -p "$OUT"

IDS="1706.03762 2104.09864 2307.08691 2502.11089 2603.12201 \
2208.07339 2211.10438 2210.17323 2306.7761 2310.18313 \
2203.02155 2305.18290 2411.15124 2501.12948 2210.03629 2310.06770 \
2602.15763 2210.02414 2507.20534 2602.02276 2607.24653"

for id in $IDS; do
  f="$OUT/$id.pdf"
  [ -s "$f" ] && { echo "skip $id"; continue; }
  if [ -n "$PROXY" ]; then
    curl -x "$PROXY" -L --max-time 90 -o "$f" "https://arxiv.org/pdf/$id"
  else
    curl -L --max-time 90 -o "$f" "https://arxiv.org/pdf/$id"
  fi
  sz=$(stat -c %s "$f" 2>/dev/null || echo 0)
  # arXiv 正常 PDF 至少 100KB，小于此视为失败
  if [ "$sz" -lt 100000 ]; then echo "FAIL $id ($sz B)"; rm -f "$f"; else echo "OK   $id ($sz B)"; fi
done
```

## 四、Python 版（走 socks5 隧道时用）

```python
import os, requests
os.environ["HTTPS_PROXY"] = "socks5h://127.0.0.1:1081"
ids = ["2602.15763", "2507.02029", "2607.24653"]
for i in ids:
    r = requests.get(f"https://arxiv.org/pdf/{i}", timeout=90)
    if r.status_code == 200 and len(r.content) > 100_000:
        open(f"{i}.pdf", "wb").write(r.content)
        print("OK", i, len(r.content))
    else:
        print("FAIL", i, r.status_code, len(r.content))
```

## 五、下载后必须验证（别信"下完了"）

1. **字节数 > 100KB**（arXiv 的 502 页面只有几百字节）
2. **文件头是 `%PDF-`**：`head -c 5 xxx.pdf`
3. **能解析**：`python -c "import pypdf; print(len(pypdf.PdfReader('x.pdf').pages))"`
4. 落盘后统计：`find . -name "*.pdf" | wc -l` 与清单条数对齐

## 六、本次失败记录（留证）

```
时间：2026-11-02 09:0x
现象：urllib 请求 arxiv.org/abs/* → URLError: Tunnel connection failed: 502 Bad Gateway
      socket.create_connection("arxiv.org",443) → OK（能连，但取不到）
      curl 任意参数 → 000
结论：沙箱出站隧道对境外站点统一 502，与本地代理无关
处置：如实标注 PDF 未落地，改交"结构化索引 + arXiv 号"
```

## 关联

- [[课程配套论文清单]]
- [[RoboBrain_论文索引]]
- [[量化_论文精读清单]]
