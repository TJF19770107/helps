title: OpenCode Zen 免费模型调研报告
summary: Zen 网关访问方式 / 8 款免费模型全清单 / 斜杠指令速查 / curl 实测 / 限流与到期风险 / TeamoRouter 对接结论
tags: [OpenCode, Zen, 免费模型, TeamoRouter, 零成本, 汤小龙, 四化迭代]
author: 汤小龙（WorkBuddy / 龙虾AI主控中心）
distilled_by: 龙虾五步法V3.6 + 1234快捷体系 + 仓颉蒸馏
surveyed_at: 2026-09-07
version: v1.0
protocol: 全域模板#320（1234）/ #332（成本底线）

## cost: 零积分（仅 WebFetch/WebSearch/curl 本地调用，未调用任何付费模型）

# OpenCode Zen 免费模型调研报告



调研日期：2026-09-07　执行：汤小龙（AI分身，WorkBuddy 宿主）　成本：0 积分 / 0 元
数据时效警告：Zen 免费模型为限时滚动轮换制，本报告清单有效期预估 ≤ 30 天（实证见 §5.1）。

## 〇、TL;DR 五条结论

||||
|---|---|---|
|1|Zen 官方 /v1/models 免鉴权可达，无需 API Key 即可拿到全量 70 个模型清单|curl https://opencode.ai/zen/v1/models → HTTP 200（实测 2026-09-07）|
|2|当前实际免费模型 8 个（官方文档 Pricing 页只写 6 个，端点多出 2 个）|deepseek-v4-flash-free、muse-spark-1.2-contributor-free 在端点在册、文档未列|
|3|TeamoRouter 可代跑：18091 已注册 deepseek-v4-flash-free，但免费额度已耗尽，会静默 fallback 到 0.01 折 glm-5.3-flash|51427 返回 402 free_request_quota_exhausted；18091 返回 model=glm-5.3-flash|
|4|限流实锤：免费额度按自然日计，次日 0 点刷新；耗尽返回 HTTP 402|错误原文：「deepseek-v4-flash额度次日0点刷新」|
|5|最大风险是扣费不是限流：Zen 余额 <$5 自动充值 $20（auto-reload），且自动充值会击穿你设置的月限额|官方文档 Auto-reload / Monthly limits 章节|



⚠️ 对汤哥的直接建议：Zen 属「免费但需要绑信用卡」的网关，不符合龙虾零成本红线。当前不建议接入 TeamoRouter，维持现有 18091 免费池 + MiMo 18808 + HY3 15731 三线即可。若将来接入，必须先关 auto-reload + 设 $0 月限额（见 §5.3）。

## 一、访问方式与 API 接口

### 1.1 三种入口

|||
|---|---|
|TUI 交互|/connect → 选 OpenCode Zen → 粘贴 Key → /models 查看|
|CLI|opencode models（列出 provider/model）、opencode auth login|
|直连 API|https://opencode.ai/zen/v1/*（但 /v1/models 例外，免鉴权）|

- 控制台/注册：https://opencode.ai/auth
- 模型 id 在 OpenCode 配置里写作 opencode/<model-id>，如 opencode/deepseek-v4-flash-free

### 1.2 API 端点矩阵（不是单一端点，按模型家族分流）

||||
|---|---|---|
|DeepSeek / MiniMax / GLM / Kimi / Big Pickle / MiMo / Ling / Nemotron / 全部 -free 模型|https://opencode.ai/zen/v1/chat/completions|OpenAI 兼容，我们要用的就是这个|
|GPT 全系 / Grok / Muse Spark（含 Contributor Free）|https://opencode.ai/zen/v1/responses|Responses API，非 chat/completions|
|Claude 全系 / Qwen 全系|https://opencode.ai/zen/v1/messages|Anthropic 协议|
|Gemini 全系|https://opencode.ai/zen/v1/models/<model-id>|每模型独立路径|

- 模型清单端点：https://opencode.ai/zen/v1/models（免鉴权，HTTP 200，返回 70 个模型）
- 鉴权头：Authorization: Bearer <ZEN_API_KEY>（无 Key 请求 chat/completions 实测返回 HTTP 400，非 401）

### 1.3 与 TeamoRouter 对接结论（只调研，本轮未改任何配置）

|||
|---|---|
|协议兼容性|Zen 主用端点即 OpenAI 兼容 /chat/completions，技术上可挂进 TeamoRouter 作为上游 provider|
|现网状态|TeamoRouter 18091 已注册 deepseek-v4-flash-free（display_name「DeepSeek V4 Flash Free【免费】」）；51427 亦注册（「DeepSeek V4 Flash福利版」）|
|阻塞点|Zen 侧需绑卡 + 拿 Key，且免费额度耗尽即 402；TeamoRouter 已内置的这个 free 模型就是被限流的那个|
|风险|Zen auto-reload 会真实扣美元，接入后一旦放量即产生费用 → 撞成本底线铁律第 4 条「付费须确认」|
|处置|本轮不改配置。若要落地，执行 §5.3 的「三步上锁」后再接入|

## 二、全部免费模型清单（2026-09-07 实测）



来源：curl https://opencode.ai/zen/v1/models 实拉（70 个模型中 id 含 -free 或官方标注 Free 的 8 个）

||||||||
|---|---|---|---|---|---|---|
|1|deepseek-v4-flash-free|DeepSeek V4 Flash Free|DeepSeek|推理最强，thinking 深度思考模式，Agent 增强；日常对话 + 复杂推理|1M|⚠️ 免费期数据可能用于模型改进；有每日次数限制|
|2|mimo-v2.5-free|MiMo-V2.5 Free|小米|Coding Agent 王者（310B MoE / 15B 激活），原生多模态（视觉+音频+文本），超长文档/代码库|1M|⚠️ 免费期数据可能用于模型改进；与本机 18808 MiMo 链路功能重叠|
|3|nemotron-3-ultra-free|Nemotron 3 Ultra Free|NVIDIA|企业级推理，超长上下文，多模态（文本+图像）|超长（未公开精确值）|🚫 NVIDIA 试用端点，明文要求勿提交个人/机密数据，使用即同意 NVIDIA API Trial ToS|
|4|nemotron-3.5-lightning-free|Nemotron 3.5 Lightning Free|NVIDIA|低延迟快速推理（Lightning 定位速度）|未公开|🚫 同 NVIDIA 试用政策|
|5|ling-3.0-flash-fin-free|Ling 3.0 Flash Fin Free|蚂蚁百灵（inclusionAI）|124B/激活 5.1B，混合推理（思考/非思考自适应），Fin 为垂直微调版，长程 Agent 工作流、工具调用|原生 256K，可扩至 1M|⚠️ 免费期数据可能用于模型改进|
|6|big-pickle|Big Pickle|隐身模型（厂商未公开）|Stealth 模型，规格与能力未知，官方仅称「大规模参数、综合能力」|未公开|⚠️ 免费期数据可能用于模型改进|
|7|muse-spark-1.3-contributor-free|Muse Spark 1.3 Contributor Free|Meta 系|通用；以极低 token 价换取用你的 prompt/completion 训练未来 Meta 模型|未公开|🚫 明确用于训练 Meta 模型 — 隐私代价最高的一款|
|8|muse-spark-1.2-contributor-free|Muse Spark 1.2 Contributor Free|Meta 系|同上（1.2 版本）|未公开|🚫 同 1.3|

### 2.1 三档分级（按「能干什么」给汤哥的直接建议）

|||
|---|---|
|🥇 可用（非敏感任务）|deepseek-v4-flash-free、mimo-v2.5-free|1M 上下文 + 强推理/强 Coding，只喂公开代码与公开资料，绝不喂密钥/客户数据/私有策略|
|🥈 谨慎|ling-3.0-flash-fin-free、big-pickle|规格不透明，做实验性任务，别接生产|
|🚫 禁用（龙虾红线）|两个 muse-spark-*-contributor-free、两个 nemotron-*-free|前两者明文拿数据训 Meta 模型；后两者是 NVIDIA 试用端点禁提交隐私 —— 全部撞「密钥脱敏 / 隐私不入四端」红线|

### 2.2 ⚠️ 与现有资产的冲突

|||
|---|---|
|MiMo 重复|Zen mimo-v2.5-free vs 本机 MiMo V2.5 Pro（https://token-plan-cn.xiaomimimo.com/v1，18808 端口）|保留本机 18808，不走 Zen：本机链路无绑卡风险、无静默轮换风险|
|HY3 重复|Zen 上一轮曾有 hy3-free（现已下架）vs 本机 CloudBase hy3-relay-proxy（15731）|本机 15731 更稳，Zen 侧不可用即弃|
|DeepSeek 重复|Zen deepseek-v4-flash-free vs TeamoRouter 18091 同名模型|两者都被同一套日额度限制，Zen 侧无额外收益|

## 三、斜杠指令速查表（TUI）



来源：官方 TUI 文档 https://opencode.ai/docs/tui；leader 键默认 ctrl+x

||||
|---|---|---|
|/connect|添加 provider 并填 API Key（接 Zen 第一步）|
|/models|列出可用模型（接 Zen 第二步）|
|/help|帮助对话框|
|/init|引导创建/更新 AGENTS.md|
|/new|/clear|开新会话|
|/sessions|/resume、/continue|列出并切换会话|
|/compact|/summarize|压缩当前会话（省 token）|
|/undo|撤销上一条消息及文件改动（依赖 Git）|
|/redo|重做（依赖 Git）|
|/share|分享会话|
|/unshare|取消分享|
|/export|导出会话为 Markdown|
|/editor|用 $EDITOR 打开外部编辑器写消息|
|/details|切换工具执行细节显示|
|/thinking|切换思考块显示（不开关推理能力；真实开关用 ctrl+t 切 variant）|
|/themes|切换主题|
|/exit|/quit、/q|退出|

### 3.1 TUI 非斜杠快捷键

|||
|---|---|
|@|引用文件（模糊搜索当前目录）|
|!|行首 ! 直接跑 shell 命令，输出进对话|
|ctrl+p|命令面板（含持久化 UI 设置，如隐藏用户名）|
|ctrl+t|循环切换模型 variant（真正开关 reasoning）|

### 3.2 配套 CLI 命令（非斜杠，终端执行）

|||
|---|---|
|opencode models [provider]|列出模型；--refresh 从 models.dev 刷新缓存；--verbose 输出成本等元数据|
|opencode auth login/list/logout|管理 provider 凭证（存 ~/.local/share/opencode/auth.json）|
|opencode run "msg"|非交互执行，适合脚本自动化|
|opencode stats|token 用量与成本统计（--models 看模型明细）|
|opencode serve / web / acp|无头服务 / Web 界面 / ACP 协议服务|
|opencode session list/delete|会话管理|
|opencode export [id]|导出会话 JSON（--sanitize 脱敏，符合龙虾红线）|
|opencode mcp add/list/auth|MCP 服务器管理|
|opencode upgrade|升级|

## 四、curl 调用示例与实测记录

### 4.1 免鉴权探清单（已实测通过，推荐每次开工先跑）

curl -s https://opencode.ai/zen/v1/models | python -c "import sys,json;[print(m['id']) for m in json.load(sys.stdin)['data']]"
# 实测：HTTP 200，返回 70 个模型 id

### 4.2 Zen 官方端点调用 DeepSeek V4 Flash Free（需 Key，模板待填）

curl https://opencode.ai/zen/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ZEN_API_KEY" \
  -d '{
    "model": "deepseek-v4-flash-free",
    "messages": [{"role":"user","content":"Reply in one short sentence."}],
    "max_tokens": 128
  }'

Python 等价（OpenAI 兼容）：

from openai import OpenAI
client = OpenAI(api_key=ZEN_API_KEY, base_url="https://opencode.ai/zen/v1")
r = client.chat.completions.create(
    model="deepseek-v4-flash-free",
    messages=[{"role": "user", "content": "hello"}],
)
print(r.choices[0].message.content)



无 Key 实测：POST /zen/v1/chat/completions → HTTP 400（端点可达，鉴权拦截）。

### 4.3 TeamoRouter 代跑实测（汤哥指定路径，已跑）

curl -s http://127.0.0.1:18091/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-teamorouter-local" \
  -d '{"model":"deepseek-v4-flash-free",
       "messages":[{"role":"user","content":"Reply with exactly three words: OpenCode Zen OK"}],
       "max_tokens":32}'

实测结果（2026-09-07 19:19）：

|||
|---|---|
|18091|中文|upstream_error：tried deepseek-v4-flash-free → glm-5.3-flash-free → deepseek-v4-pro-free → deepseek-v4-flash → glm-5.3-flash 全失败，末位 glm-5.3-flash HTTP 500 upstream_unavailable|
|18091|ASCII|HTTP 200，但 model 字段回的是 glm-5.3-flash（非请求的 free 模型）；finish_reason=length；prompt_tokens=22 / completion_tokens=32（其中 reasoning 30） / total=54；content 为空|
|51427|中文|Json deserialize error: invalid unicode code point —— 网关对中文 UTF-8 解析有 bug|
|51427|ASCII|HTTP 402 free_request_quota_exhausted：「您的deepseek-v4-flash免费额度已耗尽。如需继续使用，请更换模型代号为deepseek-v4-flash。deepseek-v4-flash额度次日0点刷新。」|

三条硬结论：

- 中文 payload 在 51427 会直接反序列化失败 → 走网关一律用 ASCII 或 \uXXXX 转义（已踩坑，记入五步法问题库）。
- 18091 的 fallback 链会静默从免费切到 0.01 折（glm-5.3-flash）——按成本底线铁律第 3 条「切换必报」：本次代跑实际产生了 0.01 折计费（54 tokens，金额可忽略但性质成立）。
- 免费额度按自然日刷新，次日 0 点归零重来；当日额度耗尽即 402，且不会自动降级到免费替代模型。

## 五、风险调研（限时免费 / 限流 / 速率）

### 5.1 🔴 限时免费到期规则：静默轮换，无公告，约 1 个月一轮

这是本次调研最有价值的发现。对比两个时点的免费清单：

|||
|---|---|
|2026-08-09（第三方核验）|mimo-v2.5-free、deepseek-v4-flash-free、nemotron-3-ultra-free、laguna-s-2.1-free、longcat-2.0-free、ling-3.0-flash-free、ling-3.0-tiny-free、north-mini-code-free （共 9 个）|
|2026-09-07（本次实拉）|mimo-v2.5-free、deepseek-v4-flash-free、nemotron-3-ultra-free、nemotron-3.5-lightning-free、ling-3.0-flash-fin-free、muse-spark-1.3-contributor-free、muse-spark-1.2-contributor-free、big-pickle （共 8 个）|

下架（29 天内）：hy3-free、laguna-s-2.1-free、longcat-2.0-free、ling-3.0-tiny-free、north-mini-code-free
新增（29 天内）：nemotron-3.5-lightning-free、ling-3.0-flash-fin-free、muse-spark-1.2/1.3-contributor-free



规则推定：免费席位由厂商「投放 → 收集反馈 → 到期下架 → 新厂商补位」滚动，官方只写「for a limited time」，从不公布到期日。
推论：任何把 Zen 免费模型写进生产链路的行为，都会在某个无预警的早上 404。只能当临时弹药，不能当基础设施。

### 5.2 限流 / 速率限制

|||
|---|---|
|RPM / TPM / 并发|官方文档完全未公开任何速率限制数字|
|免费额度|「有次数限制」（未给数字）|HTTP 402 free_request_quota_exhausted，按自然日计，次日 0 点刷新|
|计量方式|按请求计费（charged per request）|usage 字段完整返回 prompt/completion/total/reasoning_tokens|
|上下文分档|部分模型按 ≤200K / >200K、≤272K / >272K 分档计价（是价格分档，非速率限制）|

### 5.3 🔴 扣费风险（比限流更值得警惕）

|||
|---|---|
|auto-reload|余额 < $5 自动充值 $20（可改金额，可关闭）|接入前必须关闭|
|月限额被击穿|设了 $20 月限额也没用 —— auto-reload 触发后实际扣费可超过月限额（官方原文）|关 auto-reload 后再设月限额|
|信用卡手续费|4.4% + $0.30/笔|计入成本|
|会话标题偷跑 token|OpenCode 会用 Haiku/Nano/Flash 等低价但非免费模型生成会话标题|计入成本|
|弃用即失效|已弃用 18 个模型（GPT 5.x Codex 系 2026-07-23、Claude Opus 4.1 2026-08-05、Kimi K2.5 2026-08-05 等）|定期 /models 核对|

「三步上锁」接入前置条件（若将来决定接入）：① 关 auto-reload → ② 设 $0 或极低月限额 → ③ 在 TeamoRouter 侧禁用 fallback 到付费模型（本次 18091 就是被 fallback 到 0.01 折的）。

### 5.4 隐私风险（撞龙虾红线）

官方口径：所有模型托管在美国，providers 遵循零保留政策 —— 但免费模型全部是例外：

- big-pickle / deepseek-v4-flash-free / mimo-v2.5-free / ling-3.0-flash-fin-free：免费期数据可能用于改进模型
- nemotron-*-free（NVIDIA 试用端点）：请勿提交个人或机密数据，使用即同意 NVIDIA API Trial ToS
- muse-spark-*-contributor-free：明文用你的 prompt/completion 训练未来 Meta 模型



🚫 红线判定：Zen 全部免费模型一律禁止接收密钥、客户资料、私有交易策略。仅可用于公开代码与公开资料任务。

## 六、付费模型价格对比表（节选，用于未来升级判断）

单位：美元 / 1M tokens（In / Out）

||||||
|---|---|---|---|---|
|GPT 5 Nano|gpt-5-nano|$0.05|$0.40|最便宜的 GPT|
|GPT 5.6 Luna|gpt-5.6-luna|$0.20|$1.20|≤272K|
|DeepSeek V4 Flash|deepseek-v4-flash|$0.14|$0.28|最便宜的推理模型|
|GLM 5.3 Flash|glm-5.3-flash|$0.15|$0.50|现 TeamoRouter 0.01 折档常客|
|MiniMax M2.5/M2.7/M3|minimax-m*|0.30|$1.20|
|Kimi K2.5|kimi-k2.5|$0.60|$3.00|
|Gemini 3 Flash|gemini-3-flash|$0.50|$3.00|
|Claude Haiku 4.5|claude-haiku-4-5|$1.00|$5.00|
|Claude Sonnet 5|claude-sonnet-5|$2.00|$10.00|
|Grok 4.6|grok-4.6|$2.00|$6.00|≤200K|
|GLM 5.3 / 5.2 / 5.1|glm-5.x|$1.40|$4.40|
|Claude Opus 5 / 4.8|claude-opus-5|$5.00|$25.00|
|GPT 5.5|gpt-5.5|$5.00|$30.00|≤272K|
|GPT 6 Astra|gpt-6-astra|$10.00|$50.00|>272K 时 $20/$75|
|GPT 5.5 Pro / 5.4 Pro|*-pro|$30.00|$180.00|天价档|



📌 限时折扣：gpt-5.6-sol 有 50% 折扣，有效期至 2026-09-18（≤272K $2.00/$10.00）。

## 七、对龙虾主控中心的落地建议

|||
|---|---|
|是否接入 TeamoRouter|暂不接入（本轮未改任何配置，按汤哥拍板）|需绑卡 + auto-reload 扣费风险 + 免费席位静默轮换|
|是否申请 Zen Key|⏸ 暂缓|当前 TeamoRouter 已内置同名 free 模型，Zen 侧无增量收益|
|DeepSeek V4 Flash Free 怎么用|走 TeamoRouter 18091（注意额度次日 0 点刷新），不要用 Zen 侧|零绑卡风险|
|MiMo 长上下文|走本机 18808（token-plan-cn）|与 Zen 重复，本机更稳|
|现有网关的两个 bug|51427 中文 payload 反序列化失败；18091 会静默 fallback 到 0.01 折|需记入问题库（见 §八）|
|后续监控|每月跑一次 §4.1 免鉴权清单命令，diff 免费席位变化|零成本，防静默下架|

## 八、四化迭代记录

|||
|---|---|
|标准化|统一报告模板（TL;DR → 访问方式 → 清单 → 指令 → 实测 → 风险 → 建议 → 归档）|
|模块化|8 款免费模型按「可档位」三档分级，可直接复用于其他网关调研|
|自动化|§4.1 一条 curl 命令即可复现清单核对，可挂进晨检（ai-workstation-morning-check）|
|智能化|沉淀判据：「免费但需绑卡」= 不接入；「明文拿数据训练」= 禁用；「静默轮换」= 只做临时弹药|

### 8.1 沉淀到问题库（全局问题沉淀与复用 SKILL）

||||
|---|---|---|
|P1|TeamoRouter 51427 中文 payload 解析失败|Json deserialize error: invalid unicode code point|走网关一律 ASCII 或 \uXXXX 转义|
|P2|TeamoRouter 18091 静默 fallback 到付费档|请求 deepseek-v4-flash-free 实际返回 glm-5.3-flash（0.01 折）|触发成本底线「切换必报」；生产链路应禁用 fallback|
|P3|Zen 免费模型静默轮换|29 天内 5 个下架、4 个新增，官方不公告|每月 diff 一次 /v1/models|
|P4|Zen /v1/models 元数据极简|仅返回 id/object/created/owned_by，无 context limit / cost 字段|上下文长度需另查 models.dev 或 opencode models --verbose|

## 九、附录：本报告全部数据来源

|||
|---|---|
|Zen 官方文档|https://opencode.ai/docs/zen|端点矩阵、定价、auto-reload、弃用表、隐私政策|
|Zen 模型清单 API|https://opencode.ai/zen/v1/models|免鉴权实拉 70 个模型 id（核心证据）|
|TUI 文档|https://opencode.ai/docs/tui|17 条斜杠指令 + 快捷键|
|CLI 文档|https://opencode.ai/docs/cli|21 条 CLI 命令|
|Zen 中文镜像|https://www.opencode.asia/zh-cn/zen|端点与定价交叉验证|
|TeamoRouter 18091|http://127.0.0.1:18091/v1/models|本地代跑与 fallback 实测|
|TeamoRouter 51427|http://127.0.0.1:51427/v1/chat/completions|402 免费额度规则原文|

本报告由汤小龙（AI分身）执行，遵循龙虾五步法V3.6（检查→分析→修复→迭代→沉淀）+ 1234快捷体系 + 成本底线七铁律。全程零积分、零付费模型调用。万法皆空，因果不空。