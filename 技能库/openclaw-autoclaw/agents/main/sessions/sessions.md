# sessions.json

原始格式: JSON

```json
{
  "agent:main:main": {
    "sessionId": "bc4443aa-963b-4da6-921a-f7dc3e10c954",
    "updatedAt": 1776145035968,
    "systemSent": true,
    "abortedLastRun": false,
    "chatType": "direct",
    "deliveryContext": {
      "channel": "webchat"
    },
    "origin": {
      "label": "AutoClaw",
      "provider": "webchat",
      "surface": "webchat",
      "chatType": "direct"
    },
    "sessionFile": "C:\\Users\\Administrator\\.openclaw-autoclaw\\agents\\main\\sessions\\bc4443aa-963b-4da6-921a-f7dc3e10c954.jsonl",
    "compactionCount": 0,
    "skillsSnapshot": {
      "prompt": "⚠️ Skills truncated: included 68 of 83. Run `openclaw skills check` to audit.\n\n\nThe following skills provide specialized instructions for specific tasks.\nUse the read tool to load a skill's file when the task matches its description.\nWhen a skill file references a relative path, resolve it against the skill directory (parent of SKILL.md / dirname of the path) and use that absolute path in tool commands.\n\n<available_skills>\n  <skill>\n    <name>feishu-bitable</name>\n    <description>飞书多维表格（Bitable）的创建、查询、编辑和管理工具。包含 27 种字段类型支持、高级筛选、批量操作和视图管理。\n\n**当以下情况时使用此 Skill**：\n(1) 需要创建或管理飞书多维表格 App\n(2) 需要在多维表格中新增、查询、修改、删除记录（行数据）\n(3) 需要管理字段（列）、视图、数据表\n(4) 用户提到&quot;多维表格&quot;、&quot;bitable&quot;、&quot;数据表&quot;、&quot;记录&quot;、&quot;字段&quot;\n(5) 需要批量导入数据或批量更新多维表格\n</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-bitable\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-calendar</name>\n    <description>飞书日历与日程管理工具集。包含日历管理、日程管理、参会人管理、忙闲查询。\n</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-calendar\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-channel-rules</name>\n    <description>Lark/Feishu channel output rules. Always active in Lark conversations.\n</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-channel-rules\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-create-doc</name>\n    <description>创建飞书云文档。从 Lark-flavored Markdown 内容创建新的飞书云文档，支持指定创建位置（文件夹/知识库/知识空间）。\n</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-create-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-fetch-doc</name>\n    <description>获取飞书云文档内容。返回文档的 Markdown 内容，支持处理文档中的图片、文件和画板（需配合 feishu_doc_media 工具）。\n</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-fetch-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-im-read</name>\n    <description>飞书 IM 消息读取工具使用指南，覆盖会话消息获取、话题回复读取、跨会话消息搜索、图片/文件资源下载。\n\n**当以下情况时使用此 Skill**:\n(1) 需要获取群聊或单聊的历史消息\n(2) 需要读取话题（thread）内的回复消息\n(3) 需要跨会话搜索消息（按关键词、发送者、时间等条件）\n(4) 消息中包含图片、文件、音频、视频，需要下载\n(5) 用户提到&quot;聊天记录&quot;、&quot;消息&quot;、&quot;群里说了什么&quot;、&quot;话题回复&quot;、&quot;搜索消息&quot;、&quot;图片&quot;、&quot;文件下载&quot;\n(6) 需要按时间范围过滤消息、分页获取更多消息\n</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-im-read\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-task</name>\n    <description>飞书任务管理工具,用于创建、查询、更新任务和清单。\n\n**当以下情况时使用此 Skill**:\n(1) 需要创建、查询、更新、删除任务\n(2) 需要创建、管理任务清单\n(3) 需要查看任务列表或清单内的任务\n(4) 用户提到&quot;任务&quot;、&quot;待办&quot;、&quot;to-do&quot;、&quot;清单&quot;、&quot;task&quot;\n(5) 需要设置任务负责人、关注人、截止时间\n</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-task\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-troubleshoot</name>\n    <description>飞书插件问题排查工具。包含常见问题 FAQ 和深度诊断命令（/feishu_doctor）。\n\n常见问题可随时查阅。诊断命令用于排查复杂问题（多次授权仍失败、自动授权无法解决等），\n会检查账户配置、API 连通性、应用权限、用户授权状态，并生成详细的诊断报告和解决方案。\n</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-troubleshoot\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-update-doc</name>\n    <description>更新飞书云文档。支持 7 种更新模式：追加、覆盖、定位替换、全文替换、前/后插入、删除。\n</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-update-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-contact-lookup</name>\n    <description>通讯录成员查询技能，基于 MCP tool 协议封装的 `get_userlist` 接口，获取当前用户可见范围内的通讯录成员，支持按姓名/别名本地筛选匹配。返回 userid、姓名和别名。⚠️ 仅返回当前用户有权限查看的成员，非全量成员。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-contact-lookup\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-doc</name>\n    <description>文档与智能表格操作。当用户提到企业微信文档、创建文档、编辑文档、新建文档、写文档、智能表格时激活。支持文档创建/写入和智能表格的创建及子表/字段/记录写入。注意：所有文档创建和编辑请求都应使用此 skill，不要尝试用其他方式处理文档操作。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-doc-manager</name>\n    <description>企业微信文档管理技能。提供文档的创建、读取和编辑能力，支持通过 docid 或文档 URL 操作企业微信文档（doc_type=3）和智能表格（doc_type=10）。适用场景：(1) 以 Markdown 格式导出获取文档完整内容（异步轮询） (2) 新建文档或智能表格 (3) 用 Markdown 格式覆写文档内容。当用户需要查看文档内容、创建新文档、编辑文档正文时触发此 Skill。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-doc-manager\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-edit-todo</name>\n    <description>企业微信待办事项编辑技能，支持创建、更新、删除待办及变更用户处理进度状态。在用户说&quot;帮我创建一个待办&quot;、&quot;把这个任务分派给张三&quot;、&quot;标记待办完成&quot;、&quot;删掉那个待办&quot;、&quot;帮我建个提醒&quot;、&quot;更新一下待办内容&quot;、&quot;把提醒时间改到下周&quot;、&quot;接受这个待办&quot;、&quot;拒绝这个待办&quot;等需要对待办进行写操作的场景时使用。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-edit-todo\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-get-todo-detail</name>\n    <description>企业微信待办详情批量查询技能，根据待办 ID 列表获取完整信息（包含待办内容和分派人）。在用户说&quot;看看这个待办的详情&quot;、&quot;待办内容是什么&quot;、&quot;这个待办分派给谁了&quot;、&quot;告诉我待办的具体信息&quot;等需要查看待办完整内容的场景时使用。通常配合 wecom-get-todo-list 使用——先获取待办 ID 列表，再用本技能获取详情。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-get-todo-detail\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-get-todo-list</name>\n    <description>企业微信待办列表查询技能，支持按创建时间和提醒时间过滤，支持分页。在用户说&quot;看看我的待办列表&quot;、&quot;我有哪些待办&quot;、&quot;这周的待办有哪些&quot;、&quot;最近有什么待办&quot;、&quot;查一下我的待办&quot;、&quot;列出所有待办&quot;等需要浏览待办概览的场景时使用。注意：此技能仅返回待办概要信息（不含内容和分派人），如需完整详情请配合 wecom-get-todo-detail 使用。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-get-todo-list\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-meeting-create</name>\n    <description>企业微信会议创建技能, 支持创建预约会议. 当用户需要&quot;创建会议&quot;, &quot;预约会议&quot;, &quot;约会议&quot;, &quot;安排会议&quot;时触发.</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-meeting-create\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-meeting-manage</name>\n    <description>企业微信会议管理技能, 支持取消会议和更新会议受邀成员. 当用户需要&quot;取消会议&quot;, &quot;删除会议&quot;, &quot;修改会议成员&quot;, &quot;添加会议参与人&quot;, &quot;移除会议成员&quot;时触发.</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-meeting-manage\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-meeting-query</name>\n    <description>企业微信会议查询技能, 支持查询会议列表, 获取会议详情, 按关键词查找会议. 当用户需要&quot;查看会议&quot;, &quot;查询会议列表&quot;, &quot;会议详情&quot;, &quot;什么时候开会&quot;, &quot;有哪些会议&quot;, &quot;查找会议&quot;时触发.</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-meeting-query\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-msg</name>\n    <description>企业微信消息技能。提供会话列表查询、消息记录拉取和文本消息发送能力。当用户需要&quot;查看消息&quot;、&quot;看聊天记录&quot;、&quot;发消息给某人&quot;、&quot;最近有什么消息&quot;、&quot;给群里发消息&quot;时触发。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-msg\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-preflight</name>\n    <description>企业微信插件前置条件检查。在执行任何 wecom_mcp 操作前，通过 shell 命令检查工具权限配置（profile 和白名单），若缺失则自动修复并提示用户重启 Gateway。所有使用 wecom_mcp 的技能都应在首次调用前执行此检查。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-preflight\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-schedule</name>\n    <description>企业微信日程管理技能。适用于用户对企业微信日程的各类管理需求。当用户需要：(1) 查询指定时间范围内的日程列表或获取日程详细信息（标题、时间、地点、参与者等），(2) 创建新日程并设置提醒、参与人等，(3) 修改已有日程的标题、时间、地点等信息或取消日程，(4) 添加或移除日程参与人，(5) 查询多个成员的闲忙状态并分析共同空闲时段以安排会议时使用此技能。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-schedule\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-smartsheet-data</name>\n    <description>企业微信智能表格数据（记录）管理技能。提供智能表格记录的增删改查能力。适用场景：(1) 查询子表全部记录 (2) 添加一行或多行记录 (3) 更新已有记录 (4) 删除记录。当用户需要读取表格数据、写入新数据、修改或删除表格行时触发此 Skill。支持通过 docid 或文档 URL 定位文档。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-data\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-smartsheet-schema</name>\n    <description>企业微信智能表格结构管理技能。提供子表（Sheet）和字段（Field/列）的增删改查能力。适用场景：(1) 查询智能表格的子表列表 (2) 添加、更新、删除子表 (3) 查询子表的字段/列信息 (4) 添加、更新、删除字段/列。当用户需要管理智能表格的表结构、列定义、子表配置时触发此 Skill。支持通过 docid 或文档 URL 定位文档。</description>\n    <location>E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-schema\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>1password</name>\n    <description>Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in (single or multi-account), or reading/injecting/running secrets via op.</description>\n    <location>~/.openclaw-autoclaw\\skills\\1password-1.0.1\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>skill-creator</name>\n    <description>Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude&apos;s capabilities with specialized knowledge, workflows, or tool integrations.</description>\n    <location>~/.openclaw-autoclaw\\skills\\skill-creator-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>tmux</name>\n    <description>Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.</description>\n    <location>~/.openclaw-autoclaw\\skills\\tmux-1.0.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>video-frames</name>\n    <description>Extract frames or short clips from videos using ffmpeg.</description>\n    <location>~/.openclaw-autoclaw\\skills\\video-frames-1.0.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>self-reflection</name>\n    <description>Periodic self-reflection on recent sessions. Analyzes what went well, what went wrong, and writes concise, actionable insights to the appropriate workspace files. Designed to run as a cron job.</description>\n    <location>~/.openclaw-autoclaw\\skills\\agent-self-reflection-1.0.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>ai-video-editing</name>\n    <description>Chat video editor — describe your edit and the AI executes it: trim, cut, merge, add music, color grade, subtitle overlay, and export. Simple video editor with no timeline, no GUI, no learning curve. An easy video editor built for creators who think in ideas, not in keyframes. Supports conversational editing, text-based editing, and natural language video editing for no-timeline video production. Supports mp4, mov, avi, webm, mkv.\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\ai-video-editing-1.0.3\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>aminer-data-search</name>\n    <description>使用 AMiner 开放平台 API 进行学术数据查询与分析。当用户需要查询学者信息、论文详情、机构数据、期刊内容或专利信息时使用此 skill。 触发场景：提到 AMiner、学术数据查询、查论文/学者/机构/期刊/专利、学术问答搜索、引用分析、科研机构分析、学者画像、论文引用链、期刊投稿分析等。 支持 6 大组合工作流（学者全景分析、论文深度挖掘、机构研究力分析、期刊论文监控、学术智能问答、专利链分析）以及 28 个独立 API 的直接调用。 即使用户只说&quot;帮我查一下 XXX 学者&quot;或&quot;找找关于 XXX 的论文&quot;，也应主动使用此 skill。\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\aminer-open-academic-1.0.5\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>architecture-designer</name>\n    <description>Use when designing new system architecture, reviewing existing designs, or making architectural decisions. Invoke for system design, architecture review, design patterns, ADRs, scalability planning.</description>\n    <location>~/.openclaw-autoclaw\\skills\\architecture-designer-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>autoglm-browser-agent</name>\n    <description>智能浏览器自动化代理,可执行任何需要浏览器的任务。 包括但不限于:打开网页、搜索信息(百度/谷歌/必应)、浏览社交媒体(微博/小红书/知乎/抖音/B站)、 点赞/评论/转发/收藏、发帖/发消息、登录网站、填写表单、截图、采集网页内容、 在线购物比价、查看新闻资讯、操作在线文档(飞书文档/腾讯文档等)。 当用户提到任何网站名称、网址URL、或需要在网页上执行操作时,使用此技能。</description>\n    <location>~/.openclaw-autoclaw\\skills\\autoglm-browser-agent\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>autoglm-deepresearch</name>\n    <description>对用户提出的课题进行深度研究和调研，输出结构化的深度报告。当用户需要深入了解某个话题、做行业调研、专题研究、竞品分析等场景时使用此 skill。 与普通搜索不同，deepresearch 会先做少量定向搜索，再对少量关键页面进行深度阅读，过程中优先展示中间发现，最后再做总结，避免因调用次数过多导致响应过慢。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\autoglm-deepresearch\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>autoglm-file-upload</name>\n    <description>使用 AutoGLM Upload Mix 接口上传本地文件（图片、文档等）到服务器，获取文件 URL 或资源 ID，供后续接口使用。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\autoglm-file-upload\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>autoglm-generate-image</name>\n    <description>使用 AutoGLM 文生图接口，根据用户输入的文字描述生成图片。当用户需要生成图片、文字转图片、AI绘图等场景时使用此 skill。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\autoglm-generate-image\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>autoglm-image-recognition</name>\n    <description>使用 AutoGLM Image Recognition 接口识别和描述图片内容。当用户需要分析图片、识别图片中的对象、场景、文字或获取图片描述时使用此 skill。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。 若用户提供的是本地图片文件，必须先运行 upload-mix.py 将其上传并获取公网 URL，再传入本 skill。\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\autoglm-image-recognition\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>autoglm-open-link</name>\n    <description>使用 AutoGLM Open Link 接口打开指定网页并提取页面正文内容。当用户需要读取某个网页详情、提取文章全文、抓取页面正文做摘要或分析时使用此 skill。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\autoglm-open-link\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>autoglm-search-image</name>\n    <description>使用 AutoGLM 搜图接口，根据用户输入的关键词搜索相关图片。当用户需要搜索图片、查找图片素材等场景时使用此 skill。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\autoglm-search-image\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>autoglm-stock-analysis</name>\n    <description>股票分析技能（AutoGLM 版）。当用户提到任何股票、证券、基金、市场行情分析需求时必须使用此技能，包括：分析某只股票、研究公司基本面、看K线图走势、查财报数据、评估买入卖出时机、对比多只股票、分析行业板块、解读财经新闻对股价影响、用户发来图表截图等。只要涉及股票投资分析的任何问题都应触发此技能。</description>\n    <location>~/.openclaw-autoclaw\\skills\\autoglm-stock-analysis\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>autoglm-websearch</name>\n    <description>使用 AutoGLM Web Search 接口进行网络信息搜索。当用户需要联网搜索、查询最新资讯、检索网页内容或获取实时信息时使用此 skill。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\autoglm-websearch\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>automation-workflows</name>\n    <description>Design and implement automation workflows to save time and scale operations as a solopreneur. Use when identifying repetitive tasks to automate, building workflows across tools, setting up triggers and actions, or optimizing existing automations. Covers automation opportunity identification, workflow design, tool selection (Zapier, Make, n8n), testing, and maintenance. Trigger on &quot;automate&quot;, &quot;automation&quot;, &quot;workflow automation&quot;, &quot;save time&quot;, &quot;reduce manual work&quot;, &quot;automate my business&quot;, &quot;no-code automation&quot;.</description>\n    <location>~/.openclaw-autoclaw\\skills\\automation-workflows-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>backtest-expert</name>\n    <description>Expert guidance for systematic backtesting of trading strategies. Use when developing, testing, stress-testing, or validating quantitative trading strategies. Covers &quot;beating ideas to death&quot; methodology, parameter robustness testing, slippage modeling, bias prevention, and interpreting backtest results. Applicable when user asks about backtesting, strategy validation, robustness testing, avoiding overfitting, or systematic trading development.</description>\n    <location>~/.openclaw-autoclaw\\skills\\backtest-expert-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>blog-writer</name>\n    <description>This skill should be used when writing blog posts, articles, or long-form content in the writer&apos;s distinctive writing style. It produces authentic, opinionated content that matches the writer&apos;s voice—direct, conversational, and grounded in personal experience. The skill handles the complete workflow from research review through Notion publication. Use this skill for drafting blog posts, thought leadership pieces, or any writing meant to reflect the writer&apos;s perspective on AI, productivity, sales, marketing, or technology topics.</description>\n    <location>~/.openclaw-autoclaw\\skills\\blog-writer-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>brainstorming</name>\n    <description>You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.</description>\n    <location>~/.openclaw-autoclaw\\skills\\brainstorming-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>web-search</name>\n    <description>USE FOR web search. Returns ranked results with snippets, URLs, thumbnails. Supports freshness filters, SafeSearch, Goggles for custom ranking, pagination. Primary search endpoint.</description>\n    <location>~/.openclaw-autoclaw\\skills\\brave-web-search\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>clawdefender</name>\n    <description>Security scanner and input sanitizer for AI agents. Detects prompt injection, command injection, SSRF, credential exfiltration, and path traversal attacks. Use when (1) installing new skills from ClawHub, (2) processing external input like emails, calendar events, Trello cards, or API responses, (3) validating URLs before fetching, (4) running security audits on your workspace. Protects agents from malicious content in untrusted data sources.</description>\n    <location>~/.openclaw-autoclaw\\skills\\clawdefender-1\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>Code</name>\n    <description>Coding workflow with planning, implementation, verification, and testing for clean software development.</description>\n    <location>~/.openclaw-autoclaw\\skills\\code-1.0.4\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>content-strategy</name>\n    <description>Build and execute a content marketing strategy for a solopreneur business. Use when planning what content to create, deciding on content formats and channels, building a content calendar, measuring content performance, or systematizing content production. Covers audience research for content, content pillars, distribution strategy, repurposing workflows, and metrics. Trigger on &quot;content strategy&quot;, &quot;content marketing&quot;, &quot;what content should I create&quot;, &quot;content plan&quot;, &quot;content calendar&quot;, &quot;content ideas&quot;, &quot;content distribution&quot;, &quot;grow through content&quot;.</description>\n    <location>~/.openclaw-autoclaw\\skills\\content-strategy-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>copywriting</name>\n    <description>Write persuasive copy for landing pages, emails, ads, sales pages, and marketing materials. Use when you need to write headlines, CTAs, product descriptions, ad copy, email sequences, or any text meant to drive action. Covers copywriting formulas (AIDA, PAS, FAB), headline writing, emotional triggers, objection handling in copy, and A/B testing. Trigger on &quot;write copy&quot;, &quot;copywriting&quot;, &quot;landing page copy&quot;, &quot;headline&quot;, &quot;write a sales page&quot;, &quot;ad copy&quot;, &quot;email copy&quot;, &quot;persuasive writing&quot;, &quot;how to write [marketing text]&quot;.</description>\n    <location>~/.openclaw-autoclaw\\skills\\copywriting-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>desktop-control</name>\n    <description>Control desktop applications on Windows — launch, close, focus, resize, move windows, simulate keyboard/mouse input, manage processes, control VSCode, read clipboard, and capture screen info. Use when the user wants to interact with any running program, switch windows, type text, press shortcuts, open files in VSCode, manage running processes, or get system display information.</description>\n    <location>~/.openclaw-autoclaw\\skills\\desktop-control-win-1.0.1\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>docx</name>\n    <description>Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of &apos;Word doc&apos;, &apos;word document&apos;, &apos;.docx&apos;, or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a &apos;report&apos;, &apos;memo&apos;, &apos;letter&apos;, &apos;template&apos;, or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.</description>\n    <location>~/.openclaw-autoclaw\\skills\\docx\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>executing-plans</name>\n    <description>Use when you have a written implementation plan to execute in a separate session with review checkpoints</description>\n    <location>~/.openclaw-autoclaw\\skills\\executing-plans-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-chat-history</name>\n    <description>Fetch and summarize Feishu group chat history. Use when the user asks to read, review, or summarize messages from a Feishu group chat. Triggers: &quot;看群聊记录&quot;, &quot;群里聊了啥&quot;, &quot;帮我看看这个群&quot;, &quot;群消息历史&quot;, &quot;chat history&quot;, &quot;what did the group discuss&quot;. NOT for: sending messages (use message tool), reading documents (use feishu-doc skill), or wiki operations (use feishu-wiki skill).\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\feishu-chat-history\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-cron-reminder</name>\n    <description>Create cron jobs that reliably deliver reminders to Feishu (飞书) chats. Use when the user asks to set up scheduled reminders, periodic notifications, or any recurring task that should send messages to a Feishu conversation. Triggers: &apos;飞书定时提醒&apos;, &apos;定时任务发飞书&apos;, &apos;cron reminder to feishu&apos;, &apos;每小时提醒&apos;, &apos;scheduled feishu message&apos;.\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\feishu-cron-reminder\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-doc</name>\n    <description>Fetch content from Feishu (Lark) Wiki, Docs, Sheets, and Bitable. Automatically resolves Wiki URLs to real entities and converts content to Markdown.</description>\n    <location>~/.openclaw-autoclaw\\skills\\feishu-doc-1.2.7\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-perm</name>\n    <description>Feishu permission management for documents and files. Activate when user mentions sharing, permissions, collaborators.\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\feishu-perm\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-screenshot</name>\n    <description>Capture macOS screenshots and send to Feishu. Use when the user asks to take a screenshot and share it via Feishu. Triggers: &quot;截个屏发飞书&quot;, &quot;截屏&quot;, &quot;screenshot&quot;, &quot;take a screenshot and send&quot;. NOT for: sending existing files (use feishu-send-file skill), or sending text messages (use message tool).\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\feishu-screenshot\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-send-file</name>\n    <description>Send files to a Feishu group or user via REST API. Use when the user explicitly asks to send a file, attachment, or document to a Feishu chat/group. Triggers: &quot;发文件到飞书&quot;, &quot;把这个文件发到群里&quot;, &quot;send file to feishu&quot;, &quot;发个附件&quot;. NOT for: sending text messages (use message tool), sending images/screenshots (use feishu-screenshot skill), or reading documents (use feishu-doc skill).\n</description>\n    <location>~/.openclaw-autoclaw\\skills\\feishu-send-file\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>FFmpeg Video Editor</name>\n    <description>Generate FFmpeg commands from natural language video editing requests - cut, trim, convert, compress, change aspect ratio, extract audio, and more.</description>\n    <location>~/.openclaw-autoclaw\\skills\\ffmpeg-video-editor-1.0.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>find-skills</name>\n    <description>Helps users discover and install agent skills when they ask questions like &quot;how do I do X&quot;, &quot;find a skill for X&quot;, &quot;is there a skill that can...&quot;, or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.</description>\n    <location>~/.openclaw-autoclaw\\skills\\find-skills\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>frontend-design</name>\n    <description>Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when building web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.</description>\n    <location>~/.openclaw-autoclaw\\skills\\frontend-design-3-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>git-essentials</name>\n    <description>Essential Git commands and workflows for version control, branching, and collaboration.</description>\n    <location>~/.openclaw-autoclaw\\skills\\git-essentials-1.0.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>interview-designer</name>\n    <description>Analyze resumes and design interview strategies using evidence-based methodology. Transforms interview prep from &quot;read resume → ask questions&quot; into &quot;define standard → forensic evidence → future simulation&quot;. Combines Geoff Smart&apos;s Topgrading, Lou Adler&apos;s performance-based hiring, and Daniel Kahneman&apos;s bias control. Use when preparing for interviews, creating structured interview guides, or designing questions to validate candidate competencies.</description>\n    <location>~/.openclaw-autoclaw\\skills\\interview-designer-1.0.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>Market Research</name>\n    <description>Size markets, analyze competitors, and validate opportunities with practical frameworks and free data sources.</description>\n    <location>~/.openclaw-autoclaw\\skills\\market-research-1.0.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>Memory</name>\n    <description>Infinite organized memory that complements your agent&apos;s built-in memory with unlimited categorized storage.</description>\n    <location>~/.openclaw-autoclaw\\skills\\memory-1.0.2\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>obsidian-ontology-sync</name>\n    <description>Bidirectional sync between Obsidian PKM (human-friendly notes) and structured ontology (machine-queryable graph). Automatically extracts entities and relationships from markdown, maintains ontology graph, and provides feedback to improve note structure. Run sync every few hours via cron.</description>\n    <location>~/.openclaw-autoclaw\\skills\\obsidian-ontology-sync-1.0.1\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>opencode-controller</name>\n    <description>Control and operate Opencode via slash commands. Use this skill to manage sessions, select models, switch agents (plan/build), and coordinate coding through Opencode.</description>\n    <location>~/.openclaw-autoclaw\\skills\\opencode-controller-1.0.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>pdf</name>\n    <description>Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.</description>\n    <location>~/.openclaw-autoclaw\\skills\\pdf\\SKILL.md</location>\n  </skill>\n</available_skills>",
      "skills": [
        {
          "name": "feishu-bitable"
        },
        {
          "name": "feishu-calendar"
        },
        {
          "name": "feishu-channel-rules"
        },
        {
          "name": "feishu-create-doc"
        },
        {
          "name": "feishu-fetch-doc"
        },
        {
          "name": "feishu-im-read"
        },
        {
          "name": "feishu-task"
        },
        {
          "name": "feishu-troubleshoot"
        },
        {
          "name": "feishu-update-doc"
        },
        {
          "name": "wecom-contact-lookup"
        },
        {
          "name": "wecom-doc",
          "requiredEnv": []
        },
        {
          "name": "wecom-doc-manager"
        },
        {
          "name": "wecom-edit-todo"
        },
        {
          "name": "wecom-get-todo-detail"
        },
        {
          "name": "wecom-get-todo-list"
        },
        {
          "name": "wecom-meeting-create"
        },
        {
          "name": "wecom-meeting-manage"
        },
        {
          "name": "wecom-meeting-query"
        },
        {
          "name": "wecom-msg"
        },
        {
          "name": "wecom-preflight"
        },
        {
          "name": "wecom-schedule"
        },
        {
          "name": "wecom-smartsheet-data"
        },
        {
          "name": "wecom-smartsheet-schema"
        },
        {
          "name": "1password"
        },
        {
          "name": "skill-creator"
        },
        {
          "name": "tmux"
        },
        {
          "name": "video-frames"
        },
        {
          "name": "self-reflection"
        },
        {
          "name": "ai-video-editing",
          "primaryEnv": "NEMO_TOKEN",
          "requiredEnv": []
        },
        {
          "name": "aminer-data-search"
        },
        {
          "name": "architecture-designer"
        },
        {
          "name": "autoglm-browser-agent"
        },
        {
          "name": "autoglm-deepresearch"
        },
        {
          "name": "autoglm-file-upload"
        },
        {
          "name": "autoglm-generate-image"
        },
        {
          "name": "autoglm-image-recognition"
        },
        {
          "name": "autoglm-open-link"
        },
        {
          "name": "autoglm-search-image"
        },
        {
          "name": "autoglm-stock-analysis"
        },
        {
          "name": "autoglm-websearch"
        },
        {
          "name": "automation-workflows"
        },
        {
          "name": "backtest-expert"
        },
        {
          "name": "blog-writer"
        },
        {
          "name": "brainstorming"
        },
        {
          "name": "web-search"
        },
        {
          "name": "clawdefender"
        },
        {
          "name": "Code"
        },
        {
          "name": "content-strategy"
        },
        {
          "name": "copywriting"
        },
        {
          "name": "desktop-control"
        },
        {
          "name": "docx"
        },
        {
          "name": "executing-plans"
        },
        {
          "name": "feishu-chat-history"
        },
        {
          "name": "feishu-cron-reminder"
        },
        {
          "name": "feishu-doc"
        },
        {
          "name": "feishu-perm"
        },
        {
          "name": "feishu-screenshot"
        },
        {
          "name": "feishu-send-file"
        },
        {
          "name": "FFmpeg Video Editor"
        },
        {
          "name": "find-skills"
        },
        {
          "name": "frontend-design"
        },
        {
          "name": "git-essentials"
        },
        {
          "name": "interview-designer"
        },
        {
          "name": "Market Research"
        },
        {
          "name": "Memory"
        },
        {
          "name": "obsidian-ontology-sync",
          "requiredEnv": []
        },
        {
          "name": "opencode-controller"
        },
        {
          "name": "pdf"
        },
        {
          "name": "pptx"
        },
        {
          "name": "research-paper-writer"
        },
        {
          "name": "security-auditor"
        },
        {
          "name": "Self-Improving Agent (With Self-Reflection)"
        },
        {
          "name": "self-improvement"
        },
        {
          "name": "SEO (Site Audit + Content Writer + Competitor Analysis)"
        },
        {
          "name": "seo-content-writer"
        },
        {
          "name": "skill-vetter"
        },
        {
          "name": "social-content"
        },
        {
          "name": "Social Media Scheduler"
        },
        {
          "name": "supabase-postgres-best-practices"
        },
        {
          "name": "tavily-search"
        },
        {
          "name": "ui-ux-pro-max"
        },
        {
          "name": "writing-plans"
        },
        {
          "name": "xlsx"
        }
      ],
      "resolvedSkills": [
        {
          "name": "feishu-bitable",
          "description": "飞书多维表格（Bitable）的创建、查询、编辑和管理工具。包含 27 种字段类型支持、高级筛选、批量操作和视图管理。\n\n**当以下情况时使用此 Skill**：\n(1) 需要创建或管理飞书多维表格 App\n(2) 需要在多维表格中新增、查询、修改、删除记录（行数据）\n(3) 需要管理字段（列）、视图、数据表\n(4) 用户提到\"多维表格\"、\"bitable\"、\"数据表\"、\"记录\"、\"字段\"\n(5) 需要批量导入数据或批量更新多维表格\n",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-bitable\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-bitable",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-calendar",
          "description": "飞书日历与日程管理工具集。包含日历管理、日程管理、参会人管理、忙闲查询。\n",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-calendar\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-calendar",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-channel-rules",
          "description": "Lark/Feishu channel output rules. Always active in Lark conversations.\n",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-channel-rules\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-channel-rules",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-create-doc",
          "description": "创建飞书云文档。从 Lark-flavored Markdown 内容创建新的飞书云文档，支持指定创建位置（文件夹/知识库/知识空间）。\n",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-create-doc\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-create-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-fetch-doc",
          "description": "获取飞书云文档内容。返回文档的 Markdown 内容，支持处理文档中的图片、文件和画板（需配合 feishu_doc_media 工具）。\n",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-fetch-doc\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-fetch-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-im-read",
          "description": "飞书 IM 消息读取工具使用指南，覆盖会话消息获取、话题回复读取、跨会话消息搜索、图片/文件资源下载。\n\n**当以下情况时使用此 Skill**:\n(1) 需要获取群聊或单聊的历史消息\n(2) 需要读取话题（thread）内的回复消息\n(3) 需要跨会话搜索消息（按关键词、发送者、时间等条件）\n(4) 消息中包含图片、文件、音频、视频，需要下载\n(5) 用户提到\"聊天记录\"、\"消息\"、\"群里说了什么\"、\"话题回复\"、\"搜索消息\"、\"图片\"、\"文件下载\"\n(6) 需要按时间范围过滤消息、分页获取更多消息\n",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-im-read\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-im-read",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-task",
          "description": "飞书任务管理工具,用于创建、查询、更新任务和清单。\n\n**当以下情况时使用此 Skill**:\n(1) 需要创建、查询、更新、删除任务\n(2) 需要创建、管理任务清单\n(3) 需要查看任务列表或清单内的任务\n(4) 用户提到\"任务\"、\"待办\"、\"to-do\"、\"清单\"、\"task\"\n(5) 需要设置任务负责人、关注人、截止时间\n",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-task\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-task",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-troubleshoot",
          "description": "飞书插件问题排查工具。包含常见问题 FAQ 和深度诊断命令（/feishu_doctor）。\n\n常见问题可随时查阅。诊断命令用于排查复杂问题（多次授权仍失败、自动授权无法解决等），\n会检查账户配置、API 连通性、应用权限、用户授权状态，并生成详细的诊断报告和解决方案。\n",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-troubleshoot\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-troubleshoot",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-update-doc",
          "description": "更新飞书云文档。支持 7 种更新模式：追加、覆盖、定位替换、全文替换、前/后插入、删除。\n",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-update-doc\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\openclaw-lark\\skills\\feishu-update-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-contact-lookup",
          "description": "通讯录成员查询技能，基于 MCP tool 协议封装的 `get_userlist` 接口，获取当前用户可见范围内的通讯录成员，支持按姓名/别名本地筛选匹配。返回 userid、姓名和别名。⚠️ 仅返回当前用户有权限查看的成员，非全量成员。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-contact-lookup\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-contact-lookup",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-doc",
          "description": "文档与智能表格操作。当用户提到企业微信文档、创建文档、编辑文档、新建文档、写文档、智能表格时激活。支持文档创建/写入和智能表格的创建及子表/字段/记录写入。注意：所有文档创建和编辑请求都应使用此 skill，不要尝试用其他方式处理文档操作。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-doc\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-doc-manager",
          "description": "企业微信文档管理技能。提供文档的创建、读取和编辑能力，支持通过 docid 或文档 URL 操作企业微信文档（doc_type=3）和智能表格（doc_type=10）。适用场景：(1) 以 Markdown 格式导出获取文档完整内容（异步轮询） (2) 新建文档或智能表格 (3) 用 Markdown 格式覆写文档内容。当用户需要查看文档内容、创建新文档、编辑文档正文时触发此 Skill。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-doc-manager\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-doc-manager",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-edit-todo",
          "description": "企业微信待办事项编辑技能，支持创建、更新、删除待办及变更用户处理进度状态。在用户说\"帮我创建一个待办\"、\"把这个任务分派给张三\"、\"标记待办完成\"、\"删掉那个待办\"、\"帮我建个提醒\"、\"更新一下待办内容\"、\"把提醒时间改到下周\"、\"接受这个待办\"、\"拒绝这个待办\"等需要对待办进行写操作的场景时使用。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-edit-todo\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-edit-todo",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-get-todo-detail",
          "description": "企业微信待办详情批量查询技能，根据待办 ID 列表获取完整信息（包含待办内容和分派人）。在用户说\"看看这个待办的详情\"、\"待办内容是什么\"、\"这个待办分派给谁了\"、\"告诉我待办的具体信息\"等需要查看待办完整内容的场景时使用。通常配合 wecom-get-todo-list 使用——先获取待办 ID 列表，再用本技能获取详情。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-get-todo-detail\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-get-todo-detail",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-get-todo-list",
          "description": "企业微信待办列表查询技能，支持按创建时间和提醒时间过滤，支持分页。在用户说\"看看我的待办列表\"、\"我有哪些待办\"、\"这周的待办有哪些\"、\"最近有什么待办\"、\"查一下我的待办\"、\"列出所有待办\"等需要浏览待办概览的场景时使用。注意：此技能仅返回待办概要信息（不含内容和分派人），如需完整详情请配合 wecom-get-todo-detail 使用。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-get-todo-list\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-get-todo-list",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-meeting-create",
          "description": "企业微信会议创建技能, 支持创建预约会议. 当用户需要\"创建会议\", \"预约会议\", \"约会议\", \"安排会议\"时触发.",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-meeting-create\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-meeting-create",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-meeting-manage",
          "description": "企业微信会议管理技能, 支持取消会议和更新会议受邀成员. 当用户需要\"取消会议\", \"删除会议\", \"修改会议成员\", \"添加会议参与人\", \"移除会议成员\"时触发.",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-meeting-manage\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-meeting-manage",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-meeting-query",
          "description": "企业微信会议查询技能, 支持查询会议列表, 获取会议详情, 按关键词查找会议. 当用户需要\"查看会议\", \"查询会议列表\", \"会议详情\", \"什么时候开会\", \"有哪些会议\", \"查找会议\"时触发.",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-meeting-query\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-meeting-query",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-msg",
          "description": "企业微信消息技能。提供会话列表查询、消息记录拉取和文本消息发送能力。当用户需要\"查看消息\"、\"看聊天记录\"、\"发消息给某人\"、\"最近有什么消息\"、\"给群里发消息\"时触发。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-msg\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-msg",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-preflight",
          "description": "企业微信插件前置条件检查。在执行任何 wecom_mcp 操作前，通过 shell 命令检查工具权限配置（profile 和白名单），若缺失则自动修复并提示用户重启 Gateway。所有使用 wecom_mcp 的技能都应在首次调用前执行此检查。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-preflight\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-preflight",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-schedule",
          "description": "企业微信日程管理技能。适用于用户对企业微信日程的各类管理需求。当用户需要：(1) 查询指定时间范围内的日程列表或获取日程详细信息（标题、时间、地点、参与者等），(2) 创建新日程并设置提醒、参与人等，(3) 修改已有日程的标题、时间、地点等信息或取消日程，(4) 添加或移除日程参与人，(5) 查询多个成员的闲忙状态并分析共同空闲时段以安排会议时使用此技能。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-schedule\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-schedule",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-smartsheet-data",
          "description": "企业微信智能表格数据（记录）管理技能。提供智能表格记录的增删改查能力。适用场景：(1) 查询子表全部记录 (2) 添加一行或多行记录 (3) 更新已有记录 (4) 删除记录。当用户需要读取表格数据、写入新数据、修改或删除表格行时触发此 Skill。支持通过 docid 或文档 URL 定位文档。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-data\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-data",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-smartsheet-schema",
          "description": "企业微信智能表格结构管理技能。提供子表（Sheet）和字段（Field/列）的增删改查能力。适用场景：(1) 查询智能表格的子表列表 (2) 添加、更新、删除子表 (3) 查询子表的字段/列信息 (4) 添加、更新、删除字段/列。当用户需要管理智能表格的表结构、列定义、子表配置时触发此 Skill。支持通过 docid 或文档 URL 定位文档。",
          "filePath": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-schema\\SKILL.md",
          "baseDir": "E:\\AutoClaw\\resources\\gateway\\openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-schema",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "1password",
          "description": "Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in (single or multi-account), or reading/injecting/running secrets via op.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\1password-1.0.1\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\1password-1.0.1",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "skill-creator",
          "description": "Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\skill-creator-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\skill-creator-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "tmux",
          "description": "Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\tmux-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\tmux-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "video-frames",
          "description": "Extract frames or short clips from videos using ffmpeg.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\video-frames-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\video-frames-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "self-reflection",
          "description": "Periodic self-reflection on recent sessions. Analyzes what went well, what went wrong, and writes concise, actionable insights to the appropriate workspace files. Designed to run as a cron job.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\agent-self-reflection-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\agent-self-reflection-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "ai-video-editing",
          "description": "Chat video editor — describe your edit and the AI executes it: trim, cut, merge, add music, color grade, subtitle overlay, and export. Simple video editor with no timeline, no GUI, no learning curve. An easy video editor built for creators who think in ideas, not in keyframes. Supports conversational editing, text-based editing, and natural language video editing for no-timeline video production. Supports mp4, mov, avi, webm, mkv.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\ai-video-editing-1.0.3\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\ai-video-editing-1.0.3",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "aminer-data-search",
          "description": "使用 AMiner 开放平台 API 进行学术数据查询与分析。当用户需要查询学者信息、论文详情、机构数据、期刊内容或专利信息时使用此 skill。 触发场景：提到 AMiner、学术数据查询、查论文/学者/机构/期刊/专利、学术问答搜索、引用分析、科研机构分析、学者画像、论文引用链、期刊投稿分析等。 支持 6 大组合工作流（学者全景分析、论文深度挖掘、机构研究力分析、期刊论文监控、学术智能问答、专利链分析）以及 28 个独立 API 的直接调用。 即使用户只说\"帮我查一下 XXX 学者\"或\"找找关于 XXX 的论文\"，也应主动使用此 skill。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\aminer-open-academic-1.0.5\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\aminer-open-academic-1.0.5",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "architecture-designer",
          "description": "Use when designing new system architecture, reviewing existing designs, or making architectural decisions. Invoke for system design, architecture review, design patterns, ADRs, scalability planning.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\architecture-designer-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\architecture-designer-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "autoglm-browser-agent",
          "description": "智能浏览器自动化代理,可执行任何需要浏览器的任务。 包括但不限于:打开网页、搜索信息(百度/谷歌/必应)、浏览社交媒体(微博/小红书/知乎/抖音/B站)、 点赞/评论/转发/收藏、发帖/发消息、登录网站、填写表单、截图、采集网页内容、 在线购物比价、查看新闻资讯、操作在线文档(飞书文档/腾讯文档等)。 当用户提到任何网站名称、网址URL、或需要在网页上执行操作时,使用此技能。",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-browser-agent\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-browser-agent",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "autoglm-deepresearch",
          "description": "对用户提出的课题进行深度研究和调研，输出结构化的深度报告。当用户需要深入了解某个话题、做行业调研、专题研究、竞品分析等场景时使用此 skill。 与普通搜索不同，deepresearch 会先做少量定向搜索，再对少量关键页面进行深度阅读，过程中优先展示中间发现，最后再做总结，避免因调用次数过多导致响应过慢。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-deepresearch\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-deepresearch",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "autoglm-file-upload",
          "description": "使用 AutoGLM Upload Mix 接口上传本地文件（图片、文档等）到服务器，获取文件 URL 或资源 ID，供后续接口使用。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-file-upload\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-file-upload",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "autoglm-generate-image",
          "description": "使用 AutoGLM 文生图接口，根据用户输入的文字描述生成图片。当用户需要生成图片、文字转图片、AI绘图等场景时使用此 skill。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-generate-image\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-generate-image",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "autoglm-image-recognition",
          "description": "使用 AutoGLM Image Recognition 接口识别和描述图片内容。当用户需要分析图片、识别图片中的对象、场景、文字或获取图片描述时使用此 skill。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。 若用户提供的是本地图片文件，必须先运行 upload-mix.py 将其上传并获取公网 URL，再传入本 skill。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-image-recognition\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-image-recognition",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "autoglm-open-link",
          "description": "使用 AutoGLM Open Link 接口打开指定网页并提取页面正文内容。当用户需要读取某个网页详情、提取文章全文、抓取页面正文做摘要或分析时使用此 skill。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-open-link\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-open-link",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "autoglm-search-image",
          "description": "使用 AutoGLM 搜图接口，根据用户输入的关键词搜索相关图片。当用户需要搜索图片、查找图片素材等场景时使用此 skill。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-search-image\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-search-image",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "autoglm-stock-analysis",
          "description": "股票分析技能（AutoGLM 版）。当用户提到任何股票、证券、基金、市场行情分析需求时必须使用此技能，包括：分析某只股票、研究公司基本面、看K线图走势、查财报数据、评估买入卖出时机、对比多只股票、分析行业板块、解读财经新闻对股价影响、用户发来图表截图等。只要涉及股票投资分析的任何问题都应触发此技能。",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-stock-analysis\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-stock-analysis",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "autoglm-websearch",
          "description": "使用 AutoGLM Web Search 接口进行网络信息搜索。当用户需要联网搜索、查询最新资讯、检索网页内容或获取实时信息时使用此 skill。 Token 通过本地服务 http://127.0.0.1:18432/get_token 自动获取，无需手动配置环境变量。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-websearch\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\autoglm-websearch",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "automation-workflows",
          "description": "Design and implement automation workflows to save time and scale operations as a solopreneur. Use when identifying repetitive tasks to automate, building workflows across tools, setting up triggers and actions, or optimizing existing automations. Covers automation opportunity identification, workflow design, tool selection (Zapier, Make, n8n), testing, and maintenance. Trigger on \"automate\", \"automation\", \"workflow automation\", \"save time\", \"reduce manual work\", \"automate my business\", \"no-code automation\".",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\automation-workflows-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\automation-workflows-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "backtest-expert",
          "description": "Expert guidance for systematic backtesting of trading strategies. Use when developing, testing, stress-testing, or validating quantitative trading strategies. Covers \"beating ideas to death\" methodology, parameter robustness testing, slippage modeling, bias prevention, and interpreting backtest results. Applicable when user asks about backtesting, strategy validation, robustness testing, avoiding overfitting, or systematic trading development.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\backtest-expert-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\backtest-expert-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "blog-writer",
          "description": "This skill should be used when writing blog posts, articles, or long-form content in the writer's distinctive writing style. It produces authentic, opinionated content that matches the writer's voice—direct, conversational, and grounded in personal experience. The skill handles the complete workflow from research review through Notion publication. Use this skill for drafting blog posts, thought leadership pieces, or any writing meant to reflect the writer's perspective on AI, productivity, sales, marketing, or technology topics.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\blog-writer-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\blog-writer-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "brainstorming",
          "description": "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\brainstorming-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\brainstorming-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "web-search",
          "description": "USE FOR web search. Returns ranked results with snippets, URLs, thumbnails. Supports freshness filters, SafeSearch, Goggles for custom ranking, pagination. Primary search endpoint.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\brave-web-search\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\brave-web-search",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "clawdefender",
          "description": "Security scanner and input sanitizer for AI agents. Detects prompt injection, command injection, SSRF, credential exfiltration, and path traversal attacks. Use when (1) installing new skills from ClawHub, (2) processing external input like emails, calendar events, Trello cards, or API responses, (3) validating URLs before fetching, (4) running security audits on your workspace. Protects agents from malicious content in untrusted data sources.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\clawdefender-1\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\clawdefender-1",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "Code",
          "description": "Coding workflow with planning, implementation, verification, and testing for clean software development.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\code-1.0.4\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\code-1.0.4",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "content-strategy",
          "description": "Build and execute a content marketing strategy for a solopreneur business. Use when planning what content to create, deciding on content formats and channels, building a content calendar, measuring content performance, or systematizing content production. Covers audience research for content, content pillars, distribution strategy, repurposing workflows, and metrics. Trigger on \"content strategy\", \"content marketing\", \"what content should I create\", \"content plan\", \"content calendar\", \"content ideas\", \"content distribution\", \"grow through content\".",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\content-strategy-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\content-strategy-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "copywriting",
          "description": "Write persuasive copy for landing pages, emails, ads, sales pages, and marketing materials. Use when you need to write headlines, CTAs, product descriptions, ad copy, email sequences, or any text meant to drive action. Covers copywriting formulas (AIDA, PAS, FAB), headline writing, emotional triggers, objection handling in copy, and A/B testing. Trigger on \"write copy\", \"copywriting\", \"landing page copy\", \"headline\", \"write a sales page\", \"ad copy\", \"email copy\", \"persuasive writing\", \"how to write [marketing text]\".",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\copywriting-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\copywriting-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "desktop-control",
          "description": "Control desktop applications on Windows — launch, close, focus, resize, move windows, simulate keyboard/mouse input, manage processes, control VSCode, read clipboard, and capture screen info. Use when the user wants to interact with any running program, switch windows, type text, press shortcuts, open files in VSCode, manage running processes, or get system display information.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\desktop-control-win-1.0.1\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\desktop-control-win-1.0.1",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "docx",
          "description": "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\docx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\docx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "executing-plans",
          "description": "Use when you have a written implementation plan to execute in a separate session with review checkpoints",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\executing-plans-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\executing-plans-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-chat-history",
          "description": "Fetch and summarize Feishu group chat history. Use when the user asks to read, review, or summarize messages from a Feishu group chat. Triggers: \"看群聊记录\", \"群里聊了啥\", \"帮我看看这个群\", \"群消息历史\", \"chat history\", \"what did the group discuss\". NOT for: sending messages (use message tool), reading documents (use feishu-doc skill), or wiki operations (use feishu-wiki skill).\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-chat-history\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-chat-history",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-cron-reminder",
          "description": "Create cron jobs that reliably deliver reminders to Feishu (飞书) chats. Use when the user asks to set up scheduled reminders, periodic notifications, or any recurring task that should send messages to a Feishu conversation. Triggers: '飞书定时提醒', '定时任务发飞书', 'cron reminder to feishu', '每小时提醒', 'scheduled feishu message'.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-cron-reminder\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-cron-reminder",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-doc",
          "description": "Fetch content from Feishu (Lark) Wiki, Docs, Sheets, and Bitable. Automatically resolves Wiki URLs to real entities and converts content to Markdown.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-doc-1.2.7\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-doc-1.2.7",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-perm",
          "description": "Feishu permission management for documents and files. Activate when user mentions sharing, permissions, collaborators.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-perm\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-perm",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-screenshot",
          "description": "Capture macOS screenshots and send to Feishu. Use when the user asks to take a screenshot and share it via Feishu. Triggers: \"截个屏发飞书\", \"截屏\", \"screenshot\", \"take a screenshot and send\". NOT for: sending existing files (use feishu-send-file skill), or sending text messages (use message tool).\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-screenshot\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-screenshot",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-send-file",
          "description": "Send files to a Feishu group or user via REST API. Use when the user explicitly asks to send a file, attachment, or document to a Feishu chat/group. Triggers: \"发文件到飞书\", \"把这个文件发到群里\", \"send file to feishu\", \"发个附件\". NOT for: sending text messages (use message tool), sending images/screenshots (use feishu-screenshot skill), or reading documents (use feishu-doc skill).\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-send-file\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\feishu-send-file",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "FFmpeg Video Editor",
          "description": "Generate FFmpeg commands from natural language video editing requests - cut, trim, convert, compress, change aspect ratio, extract audio, and more.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\ffmpeg-video-editor-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\ffmpeg-video-editor-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "find-skills",
          "description": "Helps users discover and install agent skills when they ask questions like \"how do I do X\", \"find a skill for X\", \"is there a skill that can...\", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\find-skills\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\find-skills",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "frontend-design",
          "description": "Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when building web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\frontend-design-3-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\frontend-design-3-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "git-essentials",
          "description": "Essential Git commands and workflows for version control, branching, and collaboration.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\git-essentials-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\git-essentials-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "interview-designer",
          "description": "Analyze resumes and design interview strategies using evidence-based methodology. Transforms interview prep from \"read resume → ask questions\" into \"define standard → forensic evidence → future simulation\". Combines Geoff Smart's Topgrading, Lou Adler's performance-based hiring, and Daniel Kahneman's bias control. Use when preparing for interviews, creating structured interview guides, or designing questions to validate candidate competencies.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\interview-designer-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\interview-designer-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "Market Research",
          "description": "Size markets, analyze competitors, and validate opportunities with practical frameworks and free data sources.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\market-research-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\market-research-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "Memory",
          "description": "Infinite organized memory that complements your agent's built-in memory with unlimited categorized storage.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\memory-1.0.2\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\memory-1.0.2",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "obsidian-ontology-sync",
          "description": "Bidirectional sync between Obsidian PKM (human-friendly notes) and structured ontology (machine-queryable graph). Automatically extracts entities and relationships from markdown, maintains ontology graph, and provides feedback to improve note structure. Run sync every few hours via cron.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\obsidian-ontology-sync-1.0.1\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\obsidian-ontology-sync-1.0.1",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "opencode-controller",
          "description": "Control and operate Opencode via slash commands. Use this skill to manage sessions, select models, switch agents (plan/build), and coordinate coding through Opencode.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\opencode-controller-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\opencode-controller-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "pdf",
          "description": "Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\pdf\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\pdf",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "pptx",
          "description": "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\pptx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\pptx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "research-paper-writer",
          "description": "Creates formal academic research papers following IEEE/ACM formatting standards with proper structure, citations, and scholarly writing style. Use when the user asks to write a research paper, academic paper, or conference paper on any topic.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\research-paper-writer-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\research-paper-writer-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "security-auditor",
          "description": "Use when reviewing code for security vulnerabilities, implementing authentication flows, auditing OWASP Top 10, configuring CORS/CSP headers, handling secrets, input validation, SQL injection prevention, XSS protection, or any security-related code review.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\security-auditor-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\security-auditor-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "Self-Improving Agent (With Self-Reflection)",
          "description": "Self-reflection + Self-criticism + learning from corrections. Agent evaluates its own work, catches mistakes, and improves permanently.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\self-improving-1.1.3\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\self-improving-1.1.3",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "self-improvement",
          "description": "Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\self-improving-agent\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\self-improving-agent",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "SEO (Site Audit + Content Writer + Competitor Analysis)",
          "description": "SEO specialist agent with site audits, content writing, keyword research, technical fixes, link building, and ranking strategies.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\seo-1.0.3\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\seo-1.0.3",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "seo-content-writer",
          "description": "Use when the user asks to \"write SEO content\", \"create a blog post\", \"write an article\", \"content writing\", \"draft optimized content\", \"write me an article\", \"create a blog post about\", \"help me write SEO content\", or \"draft content for\". Creates high-quality, SEO-optimized content that ranks in search engines. Applies on-page SEO best practices, keyword optimization, and content structure for maximum visibility and engagement. For AI citation optimization, see geo-content-optimizer. For updating existing content, see content-refresher.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\seo-content-writer-2.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\seo-content-writer-2.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "skill-vetter",
          "description": "Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\skill-vetter-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\skill-vetter-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "social-content",
          "description": "When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, Facebook, or other platforms. Also use when the user mentions 'LinkedIn post,' 'Twitter thread,' 'social media,' 'content calendar,' 'social scheduling,' 'engagement,' or 'viral content.' This skill covers content creation, repurposing, and platform-specific strategies.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\social-content-generator-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\social-content-generator-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "Social Media Scheduler",
          "description": "Plan, draft, and organize social media content across platforms. Create content calendars, write platform-optimized posts, and maintain consistent posting schedules.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\social-media-scheduler-1.0.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\social-media-scheduler-1.0.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "supabase-postgres-best-practices",
          "description": "Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\supabase-postgres-best-practices\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\supabase-postgres-best-practices",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "tavily-search",
          "description": "Search the web with LLM-optimized results via the Tavily CLI. Use this skill when the user wants to search the web, find articles, look up information, get recent news, discover sources, or says \"search for\", \"find me\", \"look up\", \"what's the latest on\", \"find articles about\", or needs current information from the internet. Returns relevant results with content snippets, relevance scores, and metadata — optimized for LLM consumption. Supports domain filtering, time ranges, and multiple search depths.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\tavily-search\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\tavily-search",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "ui-ux-pro-max",
          "description": "UI/UX design intelligence and implementation guidance for building polished interfaces. Use when the user asks for UI design, UX flows, information architecture, visual style direction, design systems/tokens, component specs, copy/microcopy, accessibility, or to generate/critique/refine frontend UI (HTML/CSS/JS, React, Next.js, Vue, Svelte, Tailwind). Includes workflows for (1) generating new UI layouts and styling, (2) improving existing UI/UX, (3) producing design-system tokens and component guidelines, and (4) turning UX recommendations into concrete code changes.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\ui-ux-pro-max-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\ui-ux-pro-max-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "writing-plans",
          "description": "Use when you have a spec or requirements for a multi-step task, before touching code",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\writing-plans-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\writing-plans-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "xlsx",
          "description": "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.",
          "filePath": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\xlsx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\skills\\xlsx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        }
      ],
      "version": 0
    },
    "lastChannel": "webchat",
    "modelProvider": "zai",
    "model": "glm-5",
    "systemPromptReport": {
      "source": "run",
      "generatedAt": 1776145017277,
      "sessionId": "bc4443aa-963b-4da6-921a-f7dc3e10c954",
      "sessionKey": "agent:main:main",
      "provider": "zai",
      "model": "huawei_glm-5",
      "workspaceDir": "C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace",
      "bootstrapMaxChars": 20000,
      "bootstrapTotalMaxChars": 150000,
      "bootstrapTruncation": {
        "warningMode": "once",
        "warningShown": false,
        "truncatedFiles": 0,
        "nearLimitFiles": 0,
        "totalNearLimit": false
      },
      "sandbox": {
        "mode": "off",
        "sandboxed": false
      },
      "systemPrompt": {
        "chars": 61995,
        "projectContextChars": 16179,
        "nonProjectContextChars": 45816
      },
      "injectedWorkspaceFiles": [
        {
          "name": "AGENTS.md",
          "path": "C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace\\AGENTS.md",
          "missing": false,
          "rawChars": 9618,
          "injectedChars": 9618,
          "truncated": false
        },
        {
          "name": "SOUL.md",
          "path": "C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace\\SOUL.md",
          "missing": false,
          "rawChars": 1664,
          "injectedChars": 1664,
          "truncated": false
        },
        {
          "name": "TOOLS.md",
          "path": "C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace\\TOOLS.md",
          "missing": false,
          "rawChars": 1486,
          "injectedChars": 1486,
          "truncated": false
        },
        {
          "name": "IDENTITY.md",
          "path": "C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace\\IDENTITY.md",
          "missing": false,
          "rawChars": 633,
          "injectedChars": 633,
          "truncated": false
        },
        {
          "name": "USER.md",
          "path": "C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace\\USER.md",
          "missing": false,
          "rawChars": 474,
          "injectedChars": 474,
          "truncated": false
        },
        {
          "name": "HEARTBEAT.md",
          "path": "C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace\\HEARTBEAT.md",
          "missing": false,
          "rawChars": 167,
          "injectedChars": 167,
          "truncated": false
        },
        {
          "name": "BOOTSTRAP.md",
          "path": "C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace\\BOOTSTRAP.md",
          "missing": false,
          "rawChars": 1449,
          "injectedChars": 1449,
          "truncated": false
        }
      ],
      "skills": {
        "promptChars": 28632,
        "entries": [
          {
            "name": "feishu-bitable",
            "blockChars": 471
          },
          {
            "name": "feishu-calendar",
            "blockChars": 241
          },
          {
            "name": "feishu-channel-rules",
            "blockChars": 285
          },
          {
            "name": "feishu-create-doc",
            "blockChars": 277
          },
          {
            "name": "feishu-fetch-doc",
            "blockChars": 277
          },
          {
            "name": "feishu-im-read",
            "blockChars": 526
          },
          {
            "name": "feishu-task",
            "blockChars": 411
          },
          {
            "name": "feishu-troubleshoot",
            "blockChars": 348
          },
          {
            "name": "feishu-update-doc",
            "blockChars": 253
          },
          {
            "name": "wecom-contact-lookup",
            "blockChars": 326
          },
          {
            "name": "wecom-doc",
            "blockChars": 304
          },
          {
            "name": "wecom-doc-manager",
            "blockChars": 397
          },
          {
            "name": "wecom-edit-todo",
            "blockChars": 436
          },
          {
            "name": "wecom-get-todo-detail",
            "blockChars": 411
          },
          {
            "name": "wecom-get-todo-list",
            "blockChars": 437
          },
          {
            "name": "wecom-meeting-create",
            "blockChars": 306
          },
          {
            "name": "wecom-meeting-manage",
            "blockChars": 339
          },
          {
            "name": "wecom-meeting-query",
            "blockChars": 364
          },
          {
            "name": "wecom-msg",
            "blockChars": 319
          },
          {
            "name": "wecom-preflight",
            "blockChars": 319
          },
          {
            "name": "wecom-schedule",
            "blockChars": 373
          },
          {
            "name": "wecom-smartsheet-data",
            "blockChars": 356
          },
          {
            "name": "wecom-smartsheet-schema",
            "blockChars": 386
          },
          {
            "name": "1password",
            "blockChars": 335
          },
          {
            "name": "skill-creator",
            "blockChars": 394
          },
          {
            "name": "tmux",
            "blockChars": 242
          },
          {
            "name": "video-frames",
            "blockChars": 216
          },
          {
            "name": "self-reflection",
            "blockChars": 366
          },
          {
            "name": "ai-video-editing",
            "blockChars": 604
          },
          {
            "name": "aminer-data-search",
            "blockChars": 472
          },
          {
            "name": "architecture-designer",
            "blockChars": 377
          },
          {
            "name": "autoglm-browser-agent",
            "blockChars": 362
          },
          {
            "name": "autoglm-deepresearch",
            "blockChars": 389
          },
          {
            "name": "autoglm-file-upload",
            "blockChars": 300
          },
          {
            "name": "autoglm-generate-image",
            "blockChars": 306
          },
          {
            "name": "autoglm-image-recognition",
            "blockChars": 388
          },
          {
            "name": "autoglm-open-link",
            "blockChars": 312
          },
          {
            "name": "autoglm-search-image",
            "blockChars": 298
          },
          {
            "name": "autoglm-stock-analysis",
            "blockChars": 325
          },
          {
            "name": "autoglm-websearch",
            "blockChars": 303
          },
          {
            "name": "automation-workflows",
            "blockChars": 759
          },
          {
            "name": "backtest-expert",
            "blockChars": 624
          },
          {
            "name": "blog-writer",
            "blockChars": 708
          },
          {
            "name": "brainstorming",
            "blockChars": 361
          },
          {
            "name": "web-search",
            "blockChars": 337
          },
          {
            "name": "clawdefender",
            "blockChars": 603
          },
          {
            "name": "Code",
            "blockChars": 249
          },
          {
            "name": "content-strategy",
            "blockChars": 803
          },
          {
            "name": "copywriting",
            "blockChars": 771
          },
          {
            "name": "desktop-control",
            "blockChars": 551
          },
          {
            "name": "docx",
            "blockChars": 994
          },
          {
            "name": "executing-plans",
            "blockChars": 271
          },
          {
            "name": "feishu-chat-history",
            "blockChars": 590
          },
          {
            "name": "feishu-cron-reminder",
            "blockChars": 539
          },
          {
            "name": "feishu-doc",
            "blockChars": 306
          },
          {
            "name": "feishu-perm",
            "blockChars": 272
          },
          {
            "name": "feishu-screenshot",
            "blockChars": 497
          },
          {
            "name": "feishu-send-file",
            "blockChars": 570
          },
          {
            "name": "FFmpeg Video Editor",
            "blockChars": 322
          },
          {
            "name": "find-skills",
            "blockChars": 486
          },
          {
            "name": "frontend-design",
            "blockChars": 389
          },
          {
            "name": "git-essentials",
            "blockChars": 252
          },
          {
            "name": "interview-designer",
            "blockChars": 655
          },
          {
            "name": "Market Research",
            "blockChars": 277
          },
          {
            "name": "Memory",
            "blockChars": 261
          },
          {
            "name": "obsidian-ontology-sync",
            "blockChars": 469
          },
          {
            "name": "opencode-controller",
            "blockChars": 341
          },
          {
            "name": "pdf",
            "blockChars": 574
          }
        ]
      },
      "tools": {
        "listChars": 8087,
        "schemaChars": 40259,
        "entries": [
          {
            "name": "read",
            "summaryChars": 298,
            "schemaChars": 392,
            "propertiesCount": 4
          },
          {
            "name": "edit",
            "summaryChars": 129,
            "schemaChars": 591,
            "propertiesCount": 6
          },
          {
            "name": "write",
            "summaryChars": 127,
            "schemaChars": 313,
            "propertiesCount": 3
          },
          {
            "name": "exec",
            "summaryChars": 181,
            "schemaChars": 1086,
            "propertiesCount": 12
          },
          {
            "name": "process",
            "summaryChars": 85,
            "schemaChars": 961,
            "propertiesCount": 12
          },
          {
            "name": "browser",
            "summaryChars": 1251,
            "schemaChars": 2799,
            "propertiesCount": 48
          },
          {
            "name": "canvas",
            "summaryChars": 106,
            "schemaChars": 661,
            "propertiesCount": 18
          },
          {
            "name": "nodes",
            "summaryChars": 122,
            "schemaChars": 1800,
            "propertiesCount": 37
          },
          {
            "name": "cron",
            "summaryChars": 2689,
            "schemaChars": 690,
            "propertiesCount": 13
          },
          {
            "name": "message",
            "summaryChars": 89,
            "schemaChars": 4860,
            "propertiesCount": 91
          },
          {
            "name": "tts",
            "summaryChars": 152,
            "schemaChars": 223,
            "propertiesCount": 2
          },
          {
            "name": "gateway",
            "summaryChars": 464,
            "schemaChars": 497,
            "propertiesCount": 12
          },
          {
            "name": "agents_list",
            "summaryChars": 118,
            "schemaChars": 33,
            "propertiesCount": 0
          },
          {
            "name": "sessions_list",
            "summaryChars": 54,
            "schemaChars": 212,
            "propertiesCount": 4
          },
          {
            "name": "sessions_history",
            "summaryChars": 36,
            "schemaChars": 161,
            "propertiesCount": 3
          },
          {
            "name": "sessions_send",
            "summaryChars": 84,
            "schemaChars": 273,
            "propertiesCount": 5
          },
          {
            "name": "sessions_spawn",
            "summaryChars": 198,
            "schemaChars": 1179,
            "propertiesCount": 17
          },
          {
            "name": "subagents",
            "summaryChars": 105,
            "schemaChars": 191,
            "propertiesCount": 4
          },
          {
            "name": "session_status",
            "summaryChars": 207,
            "schemaChars": 89,
            "propertiesCount": 2
          },
          {
            "name": "web_fetch",
            "summaryChars": 129,
            "schemaChars": 374,
            "propertiesCount": 3
          },
          {
            "name": "image",
            "summaryChars": 201,
            "schemaChars": 342,
            "propertiesCount": 6
          },
          {
            "name": "pdf",
            "summaryChars": 275,
            "schemaChars": 400,
            "propertiesCount": 6
          },
          {
            "name": "feishu_get_user",
            "summaryChars": 75,
            "schemaChars": 185,
            "propertiesCount": 2
          },
          {
            "name": "feishu_search_user",
            "summaryChars": 55,
            "schemaChars": 311,
            "propertiesCount": 3
          },
          {
            "name": "feishu_chat",
            "summaryChars": 92,
            "schemaChars": 519,
            "propertiesCount": 6
          },
          {
            "name": "feishu_chat_members",
            "summaryChars": 54,
            "schemaChars": 353,
            "propertiesCount": 4
          },
          {
            "name": "feishu_im_user_message",
            "summaryChars": 402,
            "schemaChars": 1149,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_user_fetch_resource",
            "summaryChars": 456,
            "schemaChars": 371,
            "propertiesCount": 3
          },
          {
            "name": "feishu_im_user_get_messages",
            "summaryChars": 386,
            "schemaChars": 912,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_user_get_thread_messages",
            "summaryChars": 166,
            "schemaChars": 395,
            "propertiesCount": 4
          },
          {
            "name": "feishu_im_user_search_messages",
            "summaryChars": 522,
            "schemaChars": 1364,
            "propertiesCount": 12
          },
          {
            "name": "feishu_calendar_calendar",
            "summaryChars": 93,
            "schemaChars": 389,
            "propertiesCount": 4
          },
          {
            "name": "feishu_calendar_event",
            "summaryChars": 455,
            "schemaChars": 3200,
            "propertiesCount": 21
          },
          {
            "name": "feishu_calendar_event_attendee",
            "summaryChars": 117,
            "schemaChars": 1129,
            "propertiesCount": 10
          },
          {
            "name": "feishu_calendar_freebusy",
            "summaryChars": 80,
            "schemaChars": 504,
            "propertiesCount": 4
          },
          {
            "name": "feishu_task_task",
            "summaryChars": 167,
            "schemaChars": 1868,
            "propertiesCount": 15
          },
          {
            "name": "feishu_task_tasklist",
            "summaryChars": 199,
            "schemaChars": 795,
            "propertiesCount": 7
          },
          {
            "name": "feishu_task_comment",
            "summaryChars": 95,
            "schemaChars": 671,
            "propertiesCount": 9
          },
          {
            "name": "feishu_task_subtask",
            "summaryChars": 86,
            "schemaChars": 1128,
            "propertiesCount": 9
          },
          {
            "name": "feishu_bitable_app",
            "summaryChars": 139,
            "schemaChars": 511,
            "propertiesCount": 7
          },
          {
            "name": "feishu_bitable_app_table",
            "summaryChars": 320,
            "schemaChars": 1261,
            "propertiesCount": 9
          },
          {
            "name": "feishu_bitable_app_table_record",
            "summaryChars": 292,
            "schemaChars": 2381,
            "propertiesCount": 14
          },
          {
            "name": "feishu_bitable_app_table_field",
            "summaryChars": 134,
            "schemaChars": 824,
            "propertiesCount": 10
          },
          {
            "name": "feishu_bitable_app_table_view",
            "summaryChars": 125,
            "schemaChars": 701,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_bot_image",
            "summaryChars": 241,
            "schemaChars": 384,
            "propertiesCount": 3
          },
          {
            "name": "feishu_oauth",
            "summaryChars": 171,
            "schemaChars": 239,
            "propertiesCount": 1
          },
          {
            "name": "feishu_oauth_batch_auth",
            "summaryChars": 55,
            "schemaChars": 162,
            "propertiesCount": 0
          },
          {
            "name": "wecom_mcp",
            "summaryChars": 288,
            "schemaChars": 426,
            "propertiesCount": 4
          }
        ]
      }
    },
    "totalTokensFresh": true,
    "cacheRead": 0,
    "cacheWrite": 0,
    "fallbackNoticeSelectedModel": "zai/huawei_glm-5",
    "fallbackNoticeActiveModel": "zai/glm-5",
    "fallbackNoticeReason": "selected model unavailable",
    "contextTokens": 200000,
    "inputTokens": 38170,
    "outputTokens": 537,
    "totalTokens": 38170
  },
  "agent:main:session-1774247165912": {
    "sessionId": "7fa5abe2-7a24-459d-bd9a-d843a81b7804",
    "updatedAt": 1774247172802,
    "systemSent": true,
    "abortedLastRun": false,
    "chatType": "direct",
    "deliveryContext": {
      "channel": "webchat"
    },
    "lastChannel": "webchat",
    "origin": {
      "label": "ClawX",
      "provider": "webchat",
      "surface": "webchat",
      "chatType": "direct"
    },
    "sessionFile": "C:\\Users\\Administrator\\.openclaw\\agents\\main\\sessions\\7fa5abe2-7a24-459d-bd9a-d843a81b7804.jsonl",
    "compactionCount": 0,
    "skillsSnapshot": {
      "prompt": "\n\nThe following skills provide specialized instructions for specific tasks.\nUse the read tool to load a skill's file when the task matches its description.\nWhen a skill file references a relative path, resolve it against the skill directory (parent of SKILL.md / dirname of the path) and use that absolute path in tool commands.\n\n<available_skills>\n  <skill>\n    <name>feishu-bitable</name>\n    <description>飞书多维表格（Bitable）的创建、查询、编辑和管理工具。包含 27 种字段类型支持、高级筛选、批量操作和视图管理。\n\n**当以下情况时使用此 Skill**：\n(1) 需要创建或管理飞书多维表格 App\n(2) 需要在多维表格中新增、查询、修改、删除记录（行数据）\n(3) 需要管理字段（列）、视图、数据表\n(4) 用户提到&quot;多维表格&quot;、&quot;bitable&quot;、&quot;数据表&quot;、&quot;记录&quot;、&quot;字段&quot;\n(5) 需要批量导入数据或批量更新多维表格\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-bitable\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-calendar</name>\n    <description>飞书日历与日程管理工具集。包含日历管理、日程管理、参会人管理、忙闲查询。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-calendar\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-channel-rules</name>\n    <description>Lark/Feishu channel output rules. Always active in Lark conversations.\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-channel-rules\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-create-doc</name>\n    <description>创建飞书云文档。从 Lark-flavored Markdown 内容创建新的飞书云文档，支持指定创建位置（文件夹/知识库/知识空间）。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-create-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-fetch-doc</name>\n    <description>获取飞书云文档内容。返回文档的 Markdown 内容，支持处理文档中的图片、文件和画板（需配合 feishu_doc_media 工具）。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-fetch-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-im-read</name>\n    <description>飞书 IM 消息读取工具使用指南，覆盖会话消息获取、话题回复读取、跨会话消息搜索、图片/文件资源下载。\n\n**当以下情况时使用此 Skill**:\n(1) 需要获取群聊或单聊的历史消息\n(2) 需要读取话题（thread）内的回复消息\n(3) 需要跨会话搜索消息（按关键词、发送者、时间等条件）\n(4) 消息中包含图片、文件、音频、视频，需要下载\n(5) 用户提到&quot;聊天记录&quot;、&quot;消息&quot;、&quot;群里说了什么&quot;、&quot;话题回复&quot;、&quot;搜索消息&quot;、&quot;图片&quot;、&quot;文件下载&quot;\n(6) 需要按时间范围过滤消息、分页获取更多消息\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-im-read\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-task</name>\n    <description>飞书任务管理工具,用于创建、查询、更新任务和清单。\n\n**当以下情况时使用此 Skill**:\n(1) 需要创建、查询、更新、删除任务\n(2) 需要创建、管理任务清单\n(3) 需要查看任务列表或清单内的任务\n(4) 用户提到&quot;任务&quot;、&quot;待办&quot;、&quot;to-do&quot;、&quot;清单&quot;、&quot;task&quot;\n(5) 需要设置任务负责人、关注人、截止时间\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-task\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-troubleshoot</name>\n    <description>飞书插件问题排查工具。包含常见问题 FAQ 和深度诊断命令（/feishu_doctor）。\n\n常见问题可随时查阅。诊断命令用于排查复杂问题（多次授权仍失败、自动授权无法解决等），\n会检查账户配置、API 连通性、应用权限、用户授权状态，并生成详细的诊断报告和解决方案。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-troubleshoot\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-update-doc</name>\n    <description>更新飞书云文档。支持 7 种更新模式：追加、覆盖、定位替换、全文替换、前/后插入、删除。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-update-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>coding-agent</name>\n    <description>Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. Use when: (1) building/creating new features or apps, (2) reviewing PRs (spawn in temp dir), (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-liner fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat (for example spawn/run Codex or Claude Code in a Discord thread; use sessions_spawn with runtime:&quot;acp&quot;), or any work in ~/clawd workspace (never spawn agents here). Claude Code: use --print --permission-mode bypassPermissions (no PTY). Codex/Pi/OpenCode: pty:true required.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\coding-agent\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>gemini</name>\n    <description>Gemini CLI for one-shot Q&amp;A, summaries, and generation.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\gemini\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>healthcheck</name>\n    <description>Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\healthcheck\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>node-connect</name>\n    <description>Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. Use when QR/setup code/manual connect fails, local Wi-Fi works but VPS/tailnet does not, or errors mention pairing required, unauthorized, bootstrap token invalid or expired, gateway.bind, gateway.remote.url, Tailscale, or plugins.entries.device-pair.config.publicUrl.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\node-connect\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>skill-creator</name>\n    <description>Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch or when asked to improve, review, audit, tidy up, or clean up an existing skill or SKILL.md file. Also use when editing or restructuring a skill directory (moving files to references/ or scripts/, removing stale content, validating against the AgentSkills spec). Triggers on phrases like &quot;create a skill&quot;, &quot;author a skill&quot;, &quot;tidy up a skill&quot;, &quot;improve this skill&quot;, &quot;review the skill&quot;, &quot;clean up the skill&quot;, &quot;audit the skill&quot;.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\skill-creator\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>weather</name>\n    <description>Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\weather\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>web-search</name>\n    <description>USE FOR web search. Returns ranked results with snippets, URLs, thumbnails. Supports freshness filters, SafeSearch, Goggles for custom ranking, pagination. Primary search endpoint.</description>\n    <location>~/.openclaw\\skills\\brave-web-search\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>docx</name>\n    <description>Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of &apos;Word doc&apos;, &apos;word document&apos;, &apos;.docx&apos;, or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a &apos;report&apos;, &apos;memo&apos;, &apos;letter&apos;, &apos;template&apos;, or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.</description>\n    <location>~/.openclaw\\skills\\docx\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>find-skills</name>\n    <description>Helps users discover and install agent skills when they ask questions like &quot;how do I do X&quot;, &quot;find a skill for X&quot;, &quot;is there a skill that can...&quot;, or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.</description>\n    <location>~/.openclaw\\skills\\find-skills\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>pdf</name>\n    <description>Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.</description>\n    <location>~/.openclaw\\skills\\pdf\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>pptx</name>\n    <description>Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions &quot;deck,&quot; &quot;slides,&quot; &quot;presentation,&quot; or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.</description>\n    <location>~/.openclaw\\skills\\pptx\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>self-improvement</name>\n    <description>Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude (&apos;No, that&apos;s wrong...&apos;, &apos;Actually...&apos;), (3) User requests a capability that doesn&apos;t exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks.</description>\n    <location>~/.openclaw\\skills\\self-improving-agent\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>tavily-search</name>\n    <description>Search the web with LLM-optimized results via the Tavily CLI. Use this skill when the user wants to search the web, find articles, look up information, get recent news, discover sources, or says &quot;search for&quot;, &quot;find me&quot;, &quot;look up&quot;, &quot;what&apos;s the latest on&quot;, &quot;find articles about&quot;, or needs current information from the internet. Returns relevant results with content snippets, relevance scores, and metadata — optimized for LLM consumption. Supports domain filtering, time ranges, and multiple search depths.\n</description>\n    <location>~/.openclaw\\skills\\tavily-search\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>xlsx</name>\n    <description>Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like &quot;the xlsx in my downloads&quot;) — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.</description>\n    <location>~/.openclaw\\skills\\xlsx\\SKILL.md</location>\n  </skill>\n</available_skills>",
      "skills": [
        {
          "name": "feishu-bitable"
        },
        {
          "name": "feishu-calendar"
        },
        {
          "name": "feishu-channel-rules"
        },
        {
          "name": "feishu-create-doc"
        },
        {
          "name": "feishu-fetch-doc"
        },
        {
          "name": "feishu-im-read"
        },
        {
          "name": "feishu-task"
        },
        {
          "name": "feishu-troubleshoot"
        },
        {
          "name": "feishu-update-doc"
        },
        {
          "name": "coding-agent",
          "requiredEnv": []
        },
        {
          "name": "gemini",
          "requiredEnv": []
        },
        {
          "name": "healthcheck"
        },
        {
          "name": "node-connect"
        },
        {
          "name": "skill-creator"
        },
        {
          "name": "weather",
          "requiredEnv": []
        },
        {
          "name": "web-search"
        },
        {
          "name": "docx"
        },
        {
          "name": "find-skills"
        },
        {
          "name": "pdf"
        },
        {
          "name": "pptx"
        },
        {
          "name": "self-improvement"
        },
        {
          "name": "tavily-search"
        },
        {
          "name": "xlsx"
        }
      ],
      "resolvedSkills": [
        {
          "name": "feishu-bitable",
          "description": "飞书多维表格（Bitable）的创建、查询、编辑和管理工具。包含 27 种字段类型支持、高级筛选、批量操作和视图管理。\n\n**当以下情况时使用此 Skill**：\n(1) 需要创建或管理飞书多维表格 App\n(2) 需要在多维表格中新增、查询、修改、删除记录（行数据）\n(3) 需要管理字段（列）、视图、数据表\n(4) 用户提到\"多维表格\"、\"bitable\"、\"数据表\"、\"记录\"、\"字段\"\n(5) 需要批量导入数据或批量更新多维表格\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-bitable\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-bitable",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-calendar",
          "description": "飞书日历与日程管理工具集。包含日历管理、日程管理、参会人管理、忙闲查询。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-calendar\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-calendar",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-channel-rules",
          "description": "Lark/Feishu channel output rules. Always active in Lark conversations.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-channel-rules\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-channel-rules",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-create-doc",
          "description": "创建飞书云文档。从 Lark-flavored Markdown 内容创建新的飞书云文档，支持指定创建位置（文件夹/知识库/知识空间）。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-create-doc\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-create-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-fetch-doc",
          "description": "获取飞书云文档内容。返回文档的 Markdown 内容，支持处理文档中的图片、文件和画板（需配合 feishu_doc_media 工具）。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-fetch-doc\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-fetch-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-im-read",
          "description": "飞书 IM 消息读取工具使用指南，覆盖会话消息获取、话题回复读取、跨会话消息搜索、图片/文件资源下载。\n\n**当以下情况时使用此 Skill**:\n(1) 需要获取群聊或单聊的历史消息\n(2) 需要读取话题（thread）内的回复消息\n(3) 需要跨会话搜索消息（按关键词、发送者、时间等条件）\n(4) 消息中包含图片、文件、音频、视频，需要下载\n(5) 用户提到\"聊天记录\"、\"消息\"、\"群里说了什么\"、\"话题回复\"、\"搜索消息\"、\"图片\"、\"文件下载\"\n(6) 需要按时间范围过滤消息、分页获取更多消息\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-im-read\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-im-read",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-task",
          "description": "飞书任务管理工具,用于创建、查询、更新任务和清单。\n\n**当以下情况时使用此 Skill**:\n(1) 需要创建、查询、更新、删除任务\n(2) 需要创建、管理任务清单\n(3) 需要查看任务列表或清单内的任务\n(4) 用户提到\"任务\"、\"待办\"、\"to-do\"、\"清单\"、\"task\"\n(5) 需要设置任务负责人、关注人、截止时间\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-task\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-task",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-troubleshoot",
          "description": "飞书插件问题排查工具。包含常见问题 FAQ 和深度诊断命令（/feishu_doctor）。\n\n常见问题可随时查阅。诊断命令用于排查复杂问题（多次授权仍失败、自动授权无法解决等），\n会检查账户配置、API 连通性、应用权限、用户授权状态，并生成详细的诊断报告和解决方案。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-troubleshoot\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-troubleshoot",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-update-doc",
          "description": "更新飞书云文档。支持 7 种更新模式：追加、覆盖、定位替换、全文替换、前/后插入、删除。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-update-doc\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-update-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "coding-agent",
          "description": "Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. Use when: (1) building/creating new features or apps, (2) reviewing PRs (spawn in temp dir), (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-liner fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat (for example spawn/run Codex or Claude Code in a Discord thread; use sessions_spawn with runtime:\"acp\"), or any work in ~/clawd workspace (never spawn agents here). Claude Code: use --print --permission-mode bypassPermissions (no PTY). Codex/Pi/OpenCode: pty:true required.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\coding-agent\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\coding-agent",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "gemini",
          "description": "Gemini CLI for one-shot Q&A, summaries, and generation.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\gemini\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\gemini",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "healthcheck",
          "description": "Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\healthcheck\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\healthcheck",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "node-connect",
          "description": "Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. Use when QR/setup code/manual connect fails, local Wi-Fi works but VPS/tailnet does not, or errors mention pairing required, unauthorized, bootstrap token invalid or expired, gateway.bind, gateway.remote.url, Tailscale, or plugins.entries.device-pair.config.publicUrl.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\node-connect\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\node-connect",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "skill-creator",
          "description": "Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch or when asked to improve, review, audit, tidy up, or clean up an existing skill or SKILL.md file. Also use when editing or restructuring a skill directory (moving files to references/ or scripts/, removing stale content, validating against the AgentSkills spec). Triggers on phrases like \"create a skill\", \"author a skill\", \"tidy up a skill\", \"improve this skill\", \"review the skill\", \"clean up the skill\", \"audit the skill\".",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\skill-creator\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\skill-creator",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "weather",
          "description": "Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\weather\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\weather",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "web-search",
          "description": "USE FOR web search. Returns ranked results with snippets, URLs, thumbnails. Supports freshness filters, SafeSearch, Goggles for custom ranking, pagination. Primary search endpoint.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\brave-web-search\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\brave-web-search",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "docx",
          "description": "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\docx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\docx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "find-skills",
          "description": "Helps users discover and install agent skills when they ask questions like \"how do I do X\", \"find a skill for X\", \"is there a skill that can...\", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\find-skills\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\find-skills",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "pdf",
          "description": "Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\pdf\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\pdf",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "pptx",
          "description": "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\pptx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\pptx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "self-improvement",
          "description": "Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\self-improving-agent\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\self-improving-agent",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "tavily-search",
          "description": "Search the web with LLM-optimized results via the Tavily CLI. Use this skill when the user wants to search the web, find articles, look up information, get recent news, discover sources, or says \"search for\", \"find me\", \"look up\", \"what's the latest on\", \"find articles about\", or needs current information from the internet. Returns relevant results with content snippets, relevance scores, and metadata — optimized for LLM consumption. Supports domain filtering, time ranges, and multiple search depths.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\tavily-search\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\tavily-search",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "xlsx",
          "description": "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\xlsx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\xlsx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        }
      ],
      "version": 0
    },
    "authProfileOverride": "ollama-ollamac0:default",
    "authProfileOverrideSource": "auto",
    "authProfileOverrideCompactionCount": 0,
    "modelProvider": "ollama-ollamac0",
    "model": "deepseek-r1:7b",
    "contextTokens": 200000,
    "systemPromptReport": {
      "source": "run",
      "generatedAt": 1774247172717,
      "sessionId": "7fa5abe2-7a24-459d-bd9a-d843a81b7804",
      "sessionKey": "agent:main:session-1774247165912",
      "provider": "ollama-ollamac0",
      "model": "deepseek-r1:7b",
      "workspaceDir": "C:\\Users\\Administrator\\.openclaw\\workspace",
      "bootstrapMaxChars": 20000,
      "bootstrapTotalMaxChars": 150000,
      "bootstrapTruncation": {
        "warningMode": "once",
        "warningShown": false,
        "truncatedFiles": 0,
        "nearLimitFiles": 0,
        "totalNearLimit": false
      },
      "sandbox": {
        "mode": "off",
        "sandboxed": false
      },
      "systemPrompt": {
        "chars": 44302,
        "projectContextChars": 14516,
        "nonProjectContextChars": 29786
      },
      "injectedWorkspaceFiles": [
        {
          "name": "AGENTS.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\AGENTS.md",
          "missing": false,
          "rawChars": 8018,
          "injectedChars": 8018,
          "truncated": false
        },
        {
          "name": "SOUL.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\SOUL.md",
          "missing": false,
          "rawChars": 1664,
          "injectedChars": 1664,
          "truncated": false
        },
        {
          "name": "TOOLS.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\TOOLS.md",
          "missing": false,
          "rawChars": 1486,
          "injectedChars": 1486,
          "truncated": false
        },
        {
          "name": "IDENTITY.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\IDENTITY.md",
          "missing": false,
          "rawChars": 633,
          "injectedChars": 633,
          "truncated": false
        },
        {
          "name": "USER.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\USER.md",
          "missing": false,
          "rawChars": 474,
          "injectedChars": 474,
          "truncated": false
        },
        {
          "name": "HEARTBEAT.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\HEARTBEAT.md",
          "missing": false,
          "rawChars": 167,
          "injectedChars": 167,
          "truncated": false
        },
        {
          "name": "BOOTSTRAP.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\BOOTSTRAP.md",
          "missing": false,
          "rawChars": 1449,
          "injectedChars": 1449,
          "truncated": false
        }
      ],
      "skills": {
        "promptChars": 12308,
        "entries": [
          {
            "name": "feishu-bitable",
            "blockChars": 453
          },
          {
            "name": "feishu-calendar",
            "blockChars": 223
          },
          {
            "name": "feishu-channel-rules",
            "blockChars": 267
          },
          {
            "name": "feishu-create-doc",
            "blockChars": 259
          },
          {
            "name": "feishu-fetch-doc",
            "blockChars": 259
          },
          {
            "name": "feishu-im-read",
            "blockChars": 508
          },
          {
            "name": "feishu-task",
            "blockChars": 393
          },
          {
            "name": "feishu-troubleshoot",
            "blockChars": 330
          },
          {
            "name": "feishu-update-doc",
            "blockChars": 235
          },
          {
            "name": "coding-agent",
            "blockChars": 842
          },
          {
            "name": "gemini",
            "blockChars": 231
          },
          {
            "name": "healthcheck",
            "blockChars": 501
          },
          {
            "name": "node-connect",
            "blockChars": 551
          },
          {
            "name": "skill-creator",
            "blockChars": 769
          },
          {
            "name": "weather",
            "blockChars": 426
          },
          {
            "name": "web-search",
            "blockChars": 328
          },
          {
            "name": "docx",
            "blockChars": 985
          },
          {
            "name": "find-skills",
            "blockChars": 477
          },
          {
            "name": "pdf",
            "blockChars": 565
          },
          {
            "name": "pptx",
            "blockChars": 848
          },
          {
            "name": "self-improvement",
            "blockChars": 633
          },
          {
            "name": "tavily-search",
            "blockChars": 709
          },
          {
            "name": "xlsx",
            "blockChars": 1081
          }
        ]
      },
      "tools": {
        "listChars": 8116,
        "schemaChars": 40553,
        "entries": [
          {
            "name": "read",
            "summaryChars": 298,
            "schemaChars": 392,
            "propertiesCount": 4
          },
          {
            "name": "edit",
            "summaryChars": 129,
            "schemaChars": 591,
            "propertiesCount": 6
          },
          {
            "name": "write",
            "summaryChars": 127,
            "schemaChars": 313,
            "propertiesCount": 3
          },
          {
            "name": "exec",
            "summaryChars": 181,
            "schemaChars": 1086,
            "propertiesCount": 12
          },
          {
            "name": "process",
            "summaryChars": 85,
            "schemaChars": 961,
            "propertiesCount": 12
          },
          {
            "name": "browser",
            "summaryChars": 1683,
            "schemaChars": 2799,
            "propertiesCount": 48
          },
          {
            "name": "canvas",
            "summaryChars": 106,
            "schemaChars": 661,
            "propertiesCount": 18
          },
          {
            "name": "nodes",
            "summaryChars": 122,
            "schemaChars": 1800,
            "propertiesCount": 37
          },
          {
            "name": "cron",
            "summaryChars": 2689,
            "schemaChars": 690,
            "propertiesCount": 13
          },
          {
            "name": "message",
            "summaryChars": 89,
            "schemaChars": 4860,
            "propertiesCount": 91
          },
          {
            "name": "tts",
            "summaryChars": 152,
            "schemaChars": 223,
            "propertiesCount": 2
          },
          {
            "name": "gateway",
            "summaryChars": 464,
            "schemaChars": 497,
            "propertiesCount": 12
          },
          {
            "name": "agents_list",
            "summaryChars": 118,
            "schemaChars": 33,
            "propertiesCount": 0
          },
          {
            "name": "sessions_list",
            "summaryChars": 54,
            "schemaChars": 212,
            "propertiesCount": 4
          },
          {
            "name": "sessions_history",
            "summaryChars": 36,
            "schemaChars": 161,
            "propertiesCount": 3
          },
          {
            "name": "sessions_send",
            "summaryChars": 84,
            "schemaChars": 273,
            "propertiesCount": 5
          },
          {
            "name": "sessions_yield",
            "summaryChars": 97,
            "schemaChars": 60,
            "propertiesCount": 1
          },
          {
            "name": "sessions_spawn",
            "summaryChars": 198,
            "schemaChars": 1179,
            "propertiesCount": 17
          },
          {
            "name": "subagents",
            "summaryChars": 105,
            "schemaChars": 191,
            "propertiesCount": 4
          },
          {
            "name": "session_status",
            "summaryChars": 207,
            "schemaChars": 89,
            "propertiesCount": 2
          },
          {
            "name": "web_search",
            "summaryChars": 175,
            "schemaChars": 1084,
            "propertiesCount": 9
          },
          {
            "name": "web_fetch",
            "summaryChars": 129,
            "schemaChars": 374,
            "propertiesCount": 3
          },
          {
            "name": "memory_search",
            "summaryChars": 334,
            "schemaChars": 139,
            "propertiesCount": 3
          },
          {
            "name": "memory_get",
            "summaryChars": 151,
            "schemaChars": 128,
            "propertiesCount": 3
          },
          {
            "name": "feishu_get_user",
            "summaryChars": 75,
            "schemaChars": 185,
            "propertiesCount": 2
          },
          {
            "name": "feishu_search_user",
            "summaryChars": 55,
            "schemaChars": 311,
            "propertiesCount": 3
          },
          {
            "name": "feishu_chat",
            "summaryChars": 92,
            "schemaChars": 519,
            "propertiesCount": 6
          },
          {
            "name": "feishu_chat_members",
            "summaryChars": 54,
            "schemaChars": 353,
            "propertiesCount": 4
          },
          {
            "name": "feishu_im_user_message",
            "summaryChars": 402,
            "schemaChars": 1149,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_user_fetch_resource",
            "summaryChars": 456,
            "schemaChars": 371,
            "propertiesCount": 3
          },
          {
            "name": "feishu_im_user_get_messages",
            "summaryChars": 386,
            "schemaChars": 912,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_user_get_thread_messages",
            "summaryChars": 166,
            "schemaChars": 395,
            "propertiesCount": 4
          },
          {
            "name": "feishu_im_user_search_messages",
            "summaryChars": 522,
            "schemaChars": 1364,
            "propertiesCount": 12
          },
          {
            "name": "feishu_calendar_calendar",
            "summaryChars": 93,
            "schemaChars": 389,
            "propertiesCount": 4
          },
          {
            "name": "feishu_calendar_event",
            "summaryChars": 455,
            "schemaChars": 3200,
            "propertiesCount": 21
          },
          {
            "name": "feishu_calendar_event_attendee",
            "summaryChars": 117,
            "schemaChars": 1129,
            "propertiesCount": 10
          },
          {
            "name": "feishu_calendar_freebusy",
            "summaryChars": 80,
            "schemaChars": 504,
            "propertiesCount": 4
          },
          {
            "name": "feishu_task_task",
            "summaryChars": 167,
            "schemaChars": 1868,
            "propertiesCount": 15
          },
          {
            "name": "feishu_task_tasklist",
            "summaryChars": 199,
            "schemaChars": 795,
            "propertiesCount": 7
          },
          {
            "name": "feishu_task_comment",
            "summaryChars": 95,
            "schemaChars": 671,
            "propertiesCount": 9
          },
          {
            "name": "feishu_task_subtask",
            "summaryChars": 86,
            "schemaChars": 1128,
            "propertiesCount": 9
          },
          {
            "name": "feishu_bitable_app",
            "summaryChars": 139,
            "schemaChars": 511,
            "propertiesCount": 7
          },
          {
            "name": "feishu_bitable_app_table",
            "summaryChars": 320,
            "schemaChars": 1261,
            "propertiesCount": 9
          },
          {
            "name": "feishu_bitable_app_table_record",
            "summaryChars": 292,
            "schemaChars": 2381,
            "propertiesCount": 14
          },
          {
            "name": "feishu_bitable_app_table_field",
            "summaryChars": 134,
            "schemaChars": 824,
            "propertiesCount": 10
          },
          {
            "name": "feishu_bitable_app_table_view",
            "summaryChars": 125,
            "schemaChars": 701,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_bot_image",
            "summaryChars": 241,
            "schemaChars": 384,
            "propertiesCount": 3
          },
          {
            "name": "feishu_oauth",
            "summaryChars": 168,
            "schemaChars": 290,
            "propertiesCount": 1
          },
          {
            "name": "feishu_oauth_batch_auth",
            "summaryChars": 55,
            "schemaChars": 162,
            "propertiesCount": 0
          }
        ]
      }
    },
    "totalTokensFresh": false
  },
  "agent:main:session-1774248886884": {
    "sessionId": "316031d8-e03d-49f8-8ae0-64561c27d2c3",
    "updatedAt": 1774248897732,
    "systemSent": true,
    "abortedLastRun": false,
    "chatType": "direct",
    "deliveryContext": {
      "channel": "webchat"
    },
    "lastChannel": "webchat",
    "origin": {
      "label": "ClawX",
      "provider": "webchat",
      "surface": "webchat",
      "chatType": "direct"
    },
    "sessionFile": "C:\\Users\\Administrator\\.openclaw\\agents\\main\\sessions\\316031d8-e03d-49f8-8ae0-64561c27d2c3.jsonl",
    "compactionCount": 0,
    "skillsSnapshot": {
      "prompt": "\n\nThe following skills provide specialized instructions for specific tasks.\nUse the read tool to load a skill's file when the task matches its description.\nWhen a skill file references a relative path, resolve it against the skill directory (parent of SKILL.md / dirname of the path) and use that absolute path in tool commands.\n\n<available_skills>\n  <skill>\n    <name>feishu-bitable</name>\n    <description>飞书多维表格（Bitable）的创建、查询、编辑和管理工具。包含 27 种字段类型支持、高级筛选、批量操作和视图管理。\n\n**当以下情况时使用此 Skill**：\n(1) 需要创建或管理飞书多维表格 App\n(2) 需要在多维表格中新增、查询、修改、删除记录（行数据）\n(3) 需要管理字段（列）、视图、数据表\n(4) 用户提到&quot;多维表格&quot;、&quot;bitable&quot;、&quot;数据表&quot;、&quot;记录&quot;、&quot;字段&quot;\n(5) 需要批量导入数据或批量更新多维表格\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-bitable\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-calendar</name>\n    <description>飞书日历与日程管理工具集。包含日历管理、日程管理、参会人管理、忙闲查询。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-calendar\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-channel-rules</name>\n    <description>Lark/Feishu channel output rules. Always active in Lark conversations.\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-channel-rules\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-create-doc</name>\n    <description>创建飞书云文档。从 Lark-flavored Markdown 内容创建新的飞书云文档，支持指定创建位置（文件夹/知识库/知识空间）。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-create-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-fetch-doc</name>\n    <description>获取飞书云文档内容。返回文档的 Markdown 内容，支持处理文档中的图片、文件和画板（需配合 feishu_doc_media 工具）。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-fetch-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-im-read</name>\n    <description>飞书 IM 消息读取工具使用指南，覆盖会话消息获取、话题回复读取、跨会话消息搜索、图片/文件资源下载。\n\n**当以下情况时使用此 Skill**:\n(1) 需要获取群聊或单聊的历史消息\n(2) 需要读取话题（thread）内的回复消息\n(3) 需要跨会话搜索消息（按关键词、发送者、时间等条件）\n(4) 消息中包含图片、文件、音频、视频，需要下载\n(5) 用户提到&quot;聊天记录&quot;、&quot;消息&quot;、&quot;群里说了什么&quot;、&quot;话题回复&quot;、&quot;搜索消息&quot;、&quot;图片&quot;、&quot;文件下载&quot;\n(6) 需要按时间范围过滤消息、分页获取更多消息\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-im-read\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-task</name>\n    <description>飞书任务管理工具,用于创建、查询、更新任务和清单。\n\n**当以下情况时使用此 Skill**:\n(1) 需要创建、查询、更新、删除任务\n(2) 需要创建、管理任务清单\n(3) 需要查看任务列表或清单内的任务\n(4) 用户提到&quot;任务&quot;、&quot;待办&quot;、&quot;to-do&quot;、&quot;清单&quot;、&quot;task&quot;\n(5) 需要设置任务负责人、关注人、截止时间\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-task\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-troubleshoot</name>\n    <description>飞书插件问题排查工具。包含常见问题 FAQ 和深度诊断命令（/feishu_doctor）。\n\n常见问题可随时查阅。诊断命令用于排查复杂问题（多次授权仍失败、自动授权无法解决等），\n会检查账户配置、API 连通性、应用权限、用户授权状态，并生成详细的诊断报告和解决方案。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-troubleshoot\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-update-doc</name>\n    <description>更新飞书云文档。支持 7 种更新模式：追加、覆盖、定位替换、全文替换、前/后插入、删除。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-update-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-contact-lookup</name>\n    <description>通讯录成员查询技能，基于 MCP tool 协议封装的 `get_userlist` 接口，获取当前用户可见范围内的通讯录成员，支持按姓名/别名本地筛选匹配。返回 userid、姓名和别名。⚠️ 仅返回当前用户有权限查看的成员，非全量成员。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-contact-lookup\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-doc-manager</name>\n    <description>企业微信文档管理技能。提供文档的创建、读取和编辑能力，支持通过 docid 或文档 URL 操作企业微信文档（doc_type=3）和智能表格（doc_type=10）。适用场景：(1) 以 Markdown 格式导出获取文档完整内容（异步轮询） (2) 新建文档或智能表格 (3) 用 Markdown 格式覆写文档内容。当用户需要查看文档内容、创建新文档、编辑文档正文时触发此 Skill。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-doc-manager\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-edit-todo</name>\n    <description>企业微信待办事项编辑技能，支持创建、更新、删除待办及变更用户处理进度状态。在用户说&quot;帮我创建一个待办&quot;、&quot;把这个任务分派给张三&quot;、&quot;标记待办完成&quot;、&quot;删掉那个待办&quot;、&quot;帮我建个提醒&quot;、&quot;更新一下待办内容&quot;、&quot;把提醒时间改到下周&quot;、&quot;接受这个待办&quot;、&quot;拒绝这个待办&quot;等需要对待办进行写操作的场景时使用。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-edit-todo\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-get-todo-detail</name>\n    <description>企业微信待办详情批量查询技能，根据待办 ID 列表获取完整信息（包含待办内容和分派人）。在用户说&quot;看看这个待办的详情&quot;、&quot;待办内容是什么&quot;、&quot;这个待办分派给谁了&quot;、&quot;告诉我待办的具体信息&quot;等需要查看待办完整内容的场景时使用。通常配合 wecom-get-todo-list 使用——先获取待办 ID 列表，再用本技能获取详情。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-detail\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-get-todo-list</name>\n    <description>企业微信待办列表查询技能，支持按创建时间和提醒时间过滤，支持分页。在用户说&quot;看看我的待办列表&quot;、&quot;我有哪些待办&quot;、&quot;这周的待办有哪些&quot;、&quot;最近有什么待办&quot;、&quot;查一下我的待办&quot;、&quot;列出所有待办&quot;等需要浏览待办概览的场景时使用。注意：此技能仅返回待办概要信息（不含内容和分派人），如需完整详情请配合 wecom-get-todo-detail 使用。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-list\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-meeting-create</name>\n    <description>企业微信会议创建技能, 支持创建预约会议. 当用户需要&quot;创建会议&quot;, &quot;预约会议&quot;, &quot;约会议&quot;, &quot;安排会议&quot;时触发.</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-meeting-create\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-meeting-manage</name>\n    <description>企业微信会议管理技能, 支持取消会议和更新会议受邀成员. 当用户需要&quot;取消会议&quot;, &quot;删除会议&quot;, &quot;修改会议成员&quot;, &quot;添加会议参与人&quot;, &quot;移除会议成员&quot;时触发.</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-meeting-manage\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-meeting-query</name>\n    <description>企业微信会议查询技能, 支持查询会议列表, 获取会议详情, 按关键词查找会议. 当用户需要&quot;查看会议&quot;, &quot;查询会议列表&quot;, &quot;会议详情&quot;, &quot;什么时候开会&quot;, &quot;有哪些会议&quot;, &quot;查找会议&quot;时触发.</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-meeting-query\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-msg</name>\n    <description>企业微信消息技能。提供会话列表查询、消息记录拉取（支持文本/图片/文件/语音/视频）、多媒体文件获取和文本消息发送能力。当用户需要&quot;查看消息&quot;、&quot;看聊天记录&quot;、&quot;发消息给某人&quot;、&quot;最近有什么消息&quot;、&quot;给群里发消息&quot;、&quot;看看发了什么图片/文件&quot;时触发。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-msg\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-preflight</name>\n    <description>企业微信插件前置条件检查。在执行任何 wecom_mcp 操作前，通过 shell 命令检查工具权限配置（profile 和白名单），若缺失则自动修复并提示用户重启 Gateway。所有使用 wecom_mcp 的技能都应在首次调用前执行此检查。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-preflight\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-schedule</name>\n    <description>企业微信日程管理技能。适用于用户对企业微信日程的各类管理需求。当用户需要：(1) 查询指定时间范围内的日程列表或获取日程详细信息（标题、时间、地点、参与者等），(2) 创建新日程并设置提醒、参与人等，(3) 修改已有日程的标题、时间、地点等信息或取消日程，(4) 添加或移除日程参与人，(5) 查询多个成员的闲忙状态并分析共同空闲时段以安排会议时使用此技能。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-schedule\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-send-media</name>\n    <description>通过 MEDIA 指令向用户发送本地文件（图片、视频、语音等文件）。当用户要求发送或分享文件时，或当生成的文件需要交付给用户时使用。仅当通过 wecom 通道通信时使用此技能。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-send-media\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-smartsheet-data</name>\n    <description>企业微信智能表格数据（记录）管理技能。提供智能表格记录的增删改查能力。适用场景：(1) 查询子表全部记录 (2) 添加一行或多行记录 (3) 更新已有记录 (4) 删除记录。当用户需要读取表格数据、写入新数据、修改或删除表格行时触发此 Skill。支持通过 docid 或文档 URL 定位文档。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-data\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-smartsheet-schema</name>\n    <description>企业微信智能表格结构管理技能。提供子表（Sheet）和字段（Field/列）的增删改查能力。适用场景：(1) 查询智能表格的子表列表 (2) 添加、更新、删除子表 (3) 查询子表的字段/列信息 (4) 添加、更新、删除字段/列。当用户需要管理智能表格的表结构、列定义、子表配置时触发此 Skill。支持通过 docid 或文档 URL 定位文档。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-schema\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>coding-agent</name>\n    <description>Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. Use when: (1) building/creating new features or apps, (2) reviewing PRs (spawn in temp dir), (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-liner fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat (for example spawn/run Codex or Claude Code in a Discord thread; use sessions_spawn with runtime:&quot;acp&quot;), or any work in ~/clawd workspace (never spawn agents here). Claude Code: use --print --permission-mode bypassPermissions (no PTY). Codex/Pi/OpenCode: pty:true required.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\coding-agent\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>gemini</name>\n    <description>Gemini CLI for one-shot Q&amp;A, summaries, and generation.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\gemini\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>healthcheck</name>\n    <description>Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\healthcheck\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>node-connect</name>\n    <description>Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. Use when QR/setup code/manual connect fails, local Wi-Fi works but VPS/tailnet does not, or errors mention pairing required, unauthorized, bootstrap token invalid or expired, gateway.bind, gateway.remote.url, Tailscale, or plugins.entries.device-pair.config.publicUrl.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\node-connect\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>skill-creator</name>\n    <description>Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch or when asked to improve, review, audit, tidy up, or clean up an existing skill or SKILL.md file. Also use when editing or restructuring a skill directory (moving files to references/ or scripts/, removing stale content, validating against the AgentSkills spec). Triggers on phrases like &quot;create a skill&quot;, &quot;author a skill&quot;, &quot;tidy up a skill&quot;, &quot;improve this skill&quot;, &quot;review the skill&quot;, &quot;clean up the skill&quot;, &quot;audit the skill&quot;.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\skill-creator\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>weather</name>\n    <description>Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\weather\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>web-search</name>\n    <description>USE FOR web search. Returns ranked results with snippets, URLs, thumbnails. Supports freshness filters, SafeSearch, Goggles for custom ranking, pagination. Primary search endpoint.</description>\n    <location>~/.openclaw\\skills\\brave-web-search\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>docx</name>\n    <description>Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of &apos;Word doc&apos;, &apos;word document&apos;, &apos;.docx&apos;, or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a &apos;report&apos;, &apos;memo&apos;, &apos;letter&apos;, &apos;template&apos;, or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.</description>\n    <location>~/.openclaw\\skills\\docx\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>find-skills</name>\n    <description>Helps users discover and install agent skills when they ask questions like &quot;how do I do X&quot;, &quot;find a skill for X&quot;, &quot;is there a skill that can...&quot;, or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.</description>\n    <location>~/.openclaw\\skills\\find-skills\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>pdf</name>\n    <description>Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.</description>\n    <location>~/.openclaw\\skills\\pdf\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>pptx</name>\n    <description>Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions &quot;deck,&quot; &quot;slides,&quot; &quot;presentation,&quot; or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.</description>\n    <location>~/.openclaw\\skills\\pptx\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>self-improvement</name>\n    <description>Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude (&apos;No, that&apos;s wrong...&apos;, &apos;Actually...&apos;), (3) User requests a capability that doesn&apos;t exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks.</description>\n    <location>~/.openclaw\\skills\\self-improving-agent\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>tavily-search</name>\n    <description>Search the web with LLM-optimized results via the Tavily CLI. Use this skill when the user wants to search the web, find articles, look up information, get recent news, discover sources, or says &quot;search for&quot;, &quot;find me&quot;, &quot;look up&quot;, &quot;what&apos;s the latest on&quot;, &quot;find articles about&quot;, or needs current information from the internet. Returns relevant results with content snippets, relevance scores, and metadata — optimized for LLM consumption. Supports domain filtering, time ranges, and multiple search depths.\n</description>\n    <location>~/.openclaw\\skills\\tavily-search\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>xlsx</name>\n    <description>Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like &quot;the xlsx in my downloads&quot;) — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.</description>\n    <location>~/.openclaw\\skills\\xlsx\\SKILL.md</location>\n  </skill>\n</available_skills>",
      "skills": [
        {
          "name": "feishu-bitable"
        },
        {
          "name": "feishu-calendar"
        },
        {
          "name": "feishu-channel-rules"
        },
        {
          "name": "feishu-create-doc"
        },
        {
          "name": "feishu-fetch-doc"
        },
        {
          "name": "feishu-im-read"
        },
        {
          "name": "feishu-task"
        },
        {
          "name": "feishu-troubleshoot"
        },
        {
          "name": "feishu-update-doc"
        },
        {
          "name": "wecom-contact-lookup"
        },
        {
          "name": "wecom-doc-manager"
        },
        {
          "name": "wecom-edit-todo"
        },
        {
          "name": "wecom-get-todo-detail"
        },
        {
          "name": "wecom-get-todo-list"
        },
        {
          "name": "wecom-meeting-create"
        },
        {
          "name": "wecom-meeting-manage"
        },
        {
          "name": "wecom-meeting-query"
        },
        {
          "name": "wecom-msg"
        },
        {
          "name": "wecom-preflight"
        },
        {
          "name": "wecom-schedule"
        },
        {
          "name": "wecom-send-media",
          "requiredEnv": []
        },
        {
          "name": "wecom-smartsheet-data"
        },
        {
          "name": "wecom-smartsheet-schema"
        },
        {
          "name": "coding-agent",
          "requiredEnv": []
        },
        {
          "name": "gemini",
          "requiredEnv": []
        },
        {
          "name": "healthcheck"
        },
        {
          "name": "node-connect"
        },
        {
          "name": "skill-creator"
        },
        {
          "name": "weather",
          "requiredEnv": []
        },
        {
          "name": "web-search"
        },
        {
          "name": "docx"
        },
        {
          "name": "find-skills"
        },
        {
          "name": "pdf"
        },
        {
          "name": "pptx"
        },
        {
          "name": "self-improvement"
        },
        {
          "name": "tavily-search"
        },
        {
          "name": "xlsx"
        }
      ],
      "resolvedSkills": [
        {
          "name": "feishu-bitable",
          "description": "飞书多维表格（Bitable）的创建、查询、编辑和管理工具。包含 27 种字段类型支持、高级筛选、批量操作和视图管理。\n\n**当以下情况时使用此 Skill**：\n(1) 需要创建或管理飞书多维表格 App\n(2) 需要在多维表格中新增、查询、修改、删除记录（行数据）\n(3) 需要管理字段（列）、视图、数据表\n(4) 用户提到\"多维表格\"、\"bitable\"、\"数据表\"、\"记录\"、\"字段\"\n(5) 需要批量导入数据或批量更新多维表格\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-bitable\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-bitable",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-calendar",
          "description": "飞书日历与日程管理工具集。包含日历管理、日程管理、参会人管理、忙闲查询。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-calendar\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-calendar",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-channel-rules",
          "description": "Lark/Feishu channel output rules. Always active in Lark conversations.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-channel-rules\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-channel-rules",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-create-doc",
          "description": "创建飞书云文档。从 Lark-flavored Markdown 内容创建新的飞书云文档，支持指定创建位置（文件夹/知识库/知识空间）。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-create-doc\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-create-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-fetch-doc",
          "description": "获取飞书云文档内容。返回文档的 Markdown 内容，支持处理文档中的图片、文件和画板（需配合 feishu_doc_media 工具）。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-fetch-doc\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-fetch-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-im-read",
          "description": "飞书 IM 消息读取工具使用指南，覆盖会话消息获取、话题回复读取、跨会话消息搜索、图片/文件资源下载。\n\n**当以下情况时使用此 Skill**:\n(1) 需要获取群聊或单聊的历史消息\n(2) 需要读取话题（thread）内的回复消息\n(3) 需要跨会话搜索消息（按关键词、发送者、时间等条件）\n(4) 消息中包含图片、文件、音频、视频，需要下载\n(5) 用户提到\"聊天记录\"、\"消息\"、\"群里说了什么\"、\"话题回复\"、\"搜索消息\"、\"图片\"、\"文件下载\"\n(6) 需要按时间范围过滤消息、分页获取更多消息\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-im-read\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-im-read",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-task",
          "description": "飞书任务管理工具,用于创建、查询、更新任务和清单。\n\n**当以下情况时使用此 Skill**:\n(1) 需要创建、查询、更新、删除任务\n(2) 需要创建、管理任务清单\n(3) 需要查看任务列表或清单内的任务\n(4) 用户提到\"任务\"、\"待办\"、\"to-do\"、\"清单\"、\"task\"\n(5) 需要设置任务负责人、关注人、截止时间\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-task\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-task",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-troubleshoot",
          "description": "飞书插件问题排查工具。包含常见问题 FAQ 和深度诊断命令（/feishu_doctor）。\n\n常见问题可随时查阅。诊断命令用于排查复杂问题（多次授权仍失败、自动授权无法解决等），\n会检查账户配置、API 连通性、应用权限、用户授权状态，并生成详细的诊断报告和解决方案。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-troubleshoot\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-troubleshoot",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-update-doc",
          "description": "更新飞书云文档。支持 7 种更新模式：追加、覆盖、定位替换、全文替换、前/后插入、删除。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-update-doc\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-update-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-contact-lookup",
          "description": "通讯录成员查询技能，基于 MCP tool 协议封装的 `get_userlist` 接口，获取当前用户可见范围内的通讯录成员，支持按姓名/别名本地筛选匹配。返回 userid、姓名和别名。⚠️ 仅返回当前用户有权限查看的成员，非全量成员。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-contact-lookup\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-contact-lookup",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-doc-manager",
          "description": "企业微信文档管理技能。提供文档的创建、读取和编辑能力，支持通过 docid 或文档 URL 操作企业微信文档（doc_type=3）和智能表格（doc_type=10）。适用场景：(1) 以 Markdown 格式导出获取文档完整内容（异步轮询） (2) 新建文档或智能表格 (3) 用 Markdown 格式覆写文档内容。当用户需要查看文档内容、创建新文档、编辑文档正文时触发此 Skill。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-doc-manager\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-doc-manager",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-edit-todo",
          "description": "企业微信待办事项编辑技能，支持创建、更新、删除待办及变更用户处理进度状态。在用户说\"帮我创建一个待办\"、\"把这个任务分派给张三\"、\"标记待办完成\"、\"删掉那个待办\"、\"帮我建个提醒\"、\"更新一下待办内容\"、\"把提醒时间改到下周\"、\"接受这个待办\"、\"拒绝这个待办\"等需要对待办进行写操作的场景时使用。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-edit-todo\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-edit-todo",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-get-todo-detail",
          "description": "企业微信待办详情批量查询技能，根据待办 ID 列表获取完整信息（包含待办内容和分派人）。在用户说\"看看这个待办的详情\"、\"待办内容是什么\"、\"这个待办分派给谁了\"、\"告诉我待办的具体信息\"等需要查看待办完整内容的场景时使用。通常配合 wecom-get-todo-list 使用——先获取待办 ID 列表，再用本技能获取详情。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-detail\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-detail",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-get-todo-list",
          "description": "企业微信待办列表查询技能，支持按创建时间和提醒时间过滤，支持分页。在用户说\"看看我的待办列表\"、\"我有哪些待办\"、\"这周的待办有哪些\"、\"最近有什么待办\"、\"查一下我的待办\"、\"列出所有待办\"等需要浏览待办概览的场景时使用。注意：此技能仅返回待办概要信息（不含内容和分派人），如需完整详情请配合 wecom-get-todo-detail 使用。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-list\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-list",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-meeting-create",
          "description": "企业微信会议创建技能, 支持创建预约会议. 当用户需要\"创建会议\", \"预约会议\", \"约会议\", \"安排会议\"时触发.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-create\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-create",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-meeting-manage",
          "description": "企业微信会议管理技能, 支持取消会议和更新会议受邀成员. 当用户需要\"取消会议\", \"删除会议\", \"修改会议成员\", \"添加会议参与人\", \"移除会议成员\"时触发.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-manage\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-manage",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-meeting-query",
          "description": "企业微信会议查询技能, 支持查询会议列表, 获取会议详情, 按关键词查找会议. 当用户需要\"查看会议\", \"查询会议列表\", \"会议详情\", \"什么时候开会\", \"有哪些会议\", \"查找会议\"时触发.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-query\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-query",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-msg",
          "description": "企业微信消息技能。提供会话列表查询、消息记录拉取（支持文本/图片/文件/语音/视频）、多媒体文件获取和文本消息发送能力。当用户需要\"查看消息\"、\"看聊天记录\"、\"发消息给某人\"、\"最近有什么消息\"、\"给群里发消息\"、\"看看发了什么图片/文件\"时触发。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-msg\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-msg",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-preflight",
          "description": "企业微信插件前置条件检查。在执行任何 wecom_mcp 操作前，通过 shell 命令检查工具权限配置（profile 和白名单），若缺失则自动修复并提示用户重启 Gateway。所有使用 wecom_mcp 的技能都应在首次调用前执行此检查。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-preflight\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-preflight",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-schedule",
          "description": "企业微信日程管理技能。适用于用户对企业微信日程的各类管理需求。当用户需要：(1) 查询指定时间范围内的日程列表或获取日程详细信息（标题、时间、地点、参与者等），(2) 创建新日程并设置提醒、参与人等，(3) 修改已有日程的标题、时间、地点等信息或取消日程，(4) 添加或移除日程参与人，(5) 查询多个成员的闲忙状态并分析共同空闲时段以安排会议时使用此技能。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-schedule\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-schedule",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-send-media",
          "description": "通过 MEDIA 指令向用户发送本地文件（图片、视频、语音等文件）。当用户要求发送或分享文件时，或当生成的文件需要交付给用户时使用。仅当通过 wecom 通道通信时使用此技能。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-send-media\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-send-media",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-smartsheet-data",
          "description": "企业微信智能表格数据（记录）管理技能。提供智能表格记录的增删改查能力。适用场景：(1) 查询子表全部记录 (2) 添加一行或多行记录 (3) 更新已有记录 (4) 删除记录。当用户需要读取表格数据、写入新数据、修改或删除表格行时触发此 Skill。支持通过 docid 或文档 URL 定位文档。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-data\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-data",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-smartsheet-schema",
          "description": "企业微信智能表格结构管理技能。提供子表（Sheet）和字段（Field/列）的增删改查能力。适用场景：(1) 查询智能表格的子表列表 (2) 添加、更新、删除子表 (3) 查询子表的字段/列信息 (4) 添加、更新、删除字段/列。当用户需要管理智能表格的表结构、列定义、子表配置时触发此 Skill。支持通过 docid 或文档 URL 定位文档。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-schema\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-schema",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "coding-agent",
          "description": "Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. Use when: (1) building/creating new features or apps, (2) reviewing PRs (spawn in temp dir), (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-liner fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat (for example spawn/run Codex or Claude Code in a Discord thread; use sessions_spawn with runtime:\"acp\"), or any work in ~/clawd workspace (never spawn agents here). Claude Code: use --print --permission-mode bypassPermissions (no PTY). Codex/Pi/OpenCode: pty:true required.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\coding-agent\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\coding-agent",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "gemini",
          "description": "Gemini CLI for one-shot Q&A, summaries, and generation.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\gemini\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\gemini",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "healthcheck",
          "description": "Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\healthcheck\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\healthcheck",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "node-connect",
          "description": "Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. Use when QR/setup code/manual connect fails, local Wi-Fi works but VPS/tailnet does not, or errors mention pairing required, unauthorized, bootstrap token invalid or expired, gateway.bind, gateway.remote.url, Tailscale, or plugins.entries.device-pair.config.publicUrl.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\node-connect\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\node-connect",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "skill-creator",
          "description": "Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch or when asked to improve, review, audit, tidy up, or clean up an existing skill or SKILL.md file. Also use when editing or restructuring a skill directory (moving files to references/ or scripts/, removing stale content, validating against the AgentSkills spec). Triggers on phrases like \"create a skill\", \"author a skill\", \"tidy up a skill\", \"improve this skill\", \"review the skill\", \"clean up the skill\", \"audit the skill\".",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\skill-creator\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\skill-creator",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "weather",
          "description": "Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\weather\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\weather",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "web-search",
          "description": "USE FOR web search. Returns ranked results with snippets, URLs, thumbnails. Supports freshness filters, SafeSearch, Goggles for custom ranking, pagination. Primary search endpoint.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\brave-web-search\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\brave-web-search",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "docx",
          "description": "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\docx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\docx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "find-skills",
          "description": "Helps users discover and install agent skills when they ask questions like \"how do I do X\", \"find a skill for X\", \"is there a skill that can...\", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\find-skills\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\find-skills",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "pdf",
          "description": "Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\pdf\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\pdf",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "pptx",
          "description": "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\pptx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\pptx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "self-improvement",
          "description": "Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\self-improving-agent\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\self-improving-agent",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "tavily-search",
          "description": "Search the web with LLM-optimized results via the Tavily CLI. Use this skill when the user wants to search the web, find articles, look up information, get recent news, discover sources, or says \"search for\", \"find me\", \"look up\", \"what's the latest on\", \"find articles about\", or needs current information from the internet. Returns relevant results with content snippets, relevance scores, and metadata — optimized for LLM consumption. Supports domain filtering, time ranges, and multiple search depths.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\tavily-search\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\tavily-search",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "xlsx",
          "description": "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\xlsx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\xlsx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        }
      ],
      "version": 0
    },
    "authProfileOverride": "ollama-ollamac0:default",
    "authProfileOverrideSource": "auto",
    "authProfileOverrideCompactionCount": 0,
    "modelProvider": "ollama-ollamac0",
    "model": "deepseek-r1:7b",
    "contextTokens": 200000,
    "systemPromptReport": {
      "source": "run",
      "generatedAt": 1774248897627,
      "sessionId": "316031d8-e03d-49f8-8ae0-64561c27d2c3",
      "sessionKey": "agent:main:session-1774248886884",
      "provider": "ollama-ollamac0",
      "model": "deepseek-r1:7b",
      "workspaceDir": "C:\\Users\\Administrator\\.openclaw\\workspace",
      "bootstrapMaxChars": 20000,
      "bootstrapTotalMaxChars": 150000,
      "bootstrapTruncation": {
        "warningMode": "once",
        "warningShown": false,
        "truncatedFiles": 0,
        "nearLimitFiles": 0,
        "totalNearLimit": false
      },
      "sandbox": {
        "mode": "off",
        "sandboxed": false
      },
      "systemPrompt": {
        "chars": 49379,
        "projectContextChars": 14516,
        "nonProjectContextChars": 34863
      },
      "injectedWorkspaceFiles": [
        {
          "name": "AGENTS.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\AGENTS.md",
          "missing": false,
          "rawChars": 8018,
          "injectedChars": 8018,
          "truncated": false
        },
        {
          "name": "SOUL.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\SOUL.md",
          "missing": false,
          "rawChars": 1664,
          "injectedChars": 1664,
          "truncated": false
        },
        {
          "name": "TOOLS.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\TOOLS.md",
          "missing": false,
          "rawChars": 1486,
          "injectedChars": 1486,
          "truncated": false
        },
        {
          "name": "IDENTITY.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\IDENTITY.md",
          "missing": false,
          "rawChars": 633,
          "injectedChars": 633,
          "truncated": false
        },
        {
          "name": "USER.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\USER.md",
          "missing": false,
          "rawChars": 474,
          "injectedChars": 474,
          "truncated": false
        },
        {
          "name": "HEARTBEAT.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\HEARTBEAT.md",
          "missing": false,
          "rawChars": 167,
          "injectedChars": 167,
          "truncated": false
        },
        {
          "name": "BOOTSTRAP.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\BOOTSTRAP.md",
          "missing": false,
          "rawChars": 1449,
          "injectedChars": 1449,
          "truncated": false
        }
      ],
      "skills": {
        "promptChars": 17077,
        "entries": [
          {
            "name": "feishu-bitable",
            "blockChars": 453
          },
          {
            "name": "feishu-calendar",
            "blockChars": 223
          },
          {
            "name": "feishu-channel-rules",
            "blockChars": 267
          },
          {
            "name": "feishu-create-doc",
            "blockChars": 259
          },
          {
            "name": "feishu-fetch-doc",
            "blockChars": 259
          },
          {
            "name": "feishu-im-read",
            "blockChars": 508
          },
          {
            "name": "feishu-task",
            "blockChars": 393
          },
          {
            "name": "feishu-troubleshoot",
            "blockChars": 330
          },
          {
            "name": "feishu-update-doc",
            "blockChars": 235
          },
          {
            "name": "wecom-contact-lookup",
            "blockChars": 299
          },
          {
            "name": "wecom-doc-manager",
            "blockChars": 370
          },
          {
            "name": "wecom-edit-todo",
            "blockChars": 409
          },
          {
            "name": "wecom-get-todo-detail",
            "blockChars": 384
          },
          {
            "name": "wecom-get-todo-list",
            "blockChars": 410
          },
          {
            "name": "wecom-meeting-create",
            "blockChars": 279
          },
          {
            "name": "wecom-meeting-manage",
            "blockChars": 312
          },
          {
            "name": "wecom-meeting-query",
            "blockChars": 337
          },
          {
            "name": "wecom-msg",
            "blockChars": 342
          },
          {
            "name": "wecom-preflight",
            "blockChars": 292
          },
          {
            "name": "wecom-schedule",
            "blockChars": 346
          },
          {
            "name": "wecom-send-media",
            "blockChars": 259
          },
          {
            "name": "wecom-smartsheet-data",
            "blockChars": 329
          },
          {
            "name": "wecom-smartsheet-schema",
            "blockChars": 359
          },
          {
            "name": "coding-agent",
            "blockChars": 842
          },
          {
            "name": "gemini",
            "blockChars": 231
          },
          {
            "name": "healthcheck",
            "blockChars": 501
          },
          {
            "name": "node-connect",
            "blockChars": 551
          },
          {
            "name": "skill-creator",
            "blockChars": 769
          },
          {
            "name": "weather",
            "blockChars": 426
          },
          {
            "name": "web-search",
            "blockChars": 328
          },
          {
            "name": "docx",
            "blockChars": 985
          },
          {
            "name": "find-skills",
            "blockChars": 477
          },
          {
            "name": "pdf",
            "blockChars": 565
          },
          {
            "name": "pptx",
            "blockChars": 848
          },
          {
            "name": "self-improvement",
            "blockChars": 633
          },
          {
            "name": "tavily-search",
            "blockChars": 709
          },
          {
            "name": "xlsx",
            "blockChars": 1081
          }
        ]
      },
      "tools": {
        "listChars": 8418,
        "schemaChars": 40979,
        "entries": [
          {
            "name": "read",
            "summaryChars": 298,
            "schemaChars": 392,
            "propertiesCount": 4
          },
          {
            "name": "edit",
            "summaryChars": 129,
            "schemaChars": 591,
            "propertiesCount": 6
          },
          {
            "name": "write",
            "summaryChars": 127,
            "schemaChars": 313,
            "propertiesCount": 3
          },
          {
            "name": "exec",
            "summaryChars": 181,
            "schemaChars": 1086,
            "propertiesCount": 12
          },
          {
            "name": "process",
            "summaryChars": 85,
            "schemaChars": 961,
            "propertiesCount": 12
          },
          {
            "name": "browser",
            "summaryChars": 1683,
            "schemaChars": 2799,
            "propertiesCount": 48
          },
          {
            "name": "canvas",
            "summaryChars": 106,
            "schemaChars": 661,
            "propertiesCount": 18
          },
          {
            "name": "nodes",
            "summaryChars": 122,
            "schemaChars": 1800,
            "propertiesCount": 37
          },
          {
            "name": "cron",
            "summaryChars": 2689,
            "schemaChars": 690,
            "propertiesCount": 13
          },
          {
            "name": "message",
            "summaryChars": 89,
            "schemaChars": 4860,
            "propertiesCount": 91
          },
          {
            "name": "tts",
            "summaryChars": 152,
            "schemaChars": 223,
            "propertiesCount": 2
          },
          {
            "name": "gateway",
            "summaryChars": 464,
            "schemaChars": 497,
            "propertiesCount": 12
          },
          {
            "name": "agents_list",
            "summaryChars": 118,
            "schemaChars": 33,
            "propertiesCount": 0
          },
          {
            "name": "sessions_list",
            "summaryChars": 54,
            "schemaChars": 212,
            "propertiesCount": 4
          },
          {
            "name": "sessions_history",
            "summaryChars": 36,
            "schemaChars": 161,
            "propertiesCount": 3
          },
          {
            "name": "sessions_send",
            "summaryChars": 84,
            "schemaChars": 273,
            "propertiesCount": 5
          },
          {
            "name": "sessions_yield",
            "summaryChars": 97,
            "schemaChars": 60,
            "propertiesCount": 1
          },
          {
            "name": "sessions_spawn",
            "summaryChars": 198,
            "schemaChars": 1179,
            "propertiesCount": 17
          },
          {
            "name": "subagents",
            "summaryChars": 105,
            "schemaChars": 191,
            "propertiesCount": 4
          },
          {
            "name": "session_status",
            "summaryChars": 207,
            "schemaChars": 89,
            "propertiesCount": 2
          },
          {
            "name": "web_search",
            "summaryChars": 175,
            "schemaChars": 1084,
            "propertiesCount": 9
          },
          {
            "name": "web_fetch",
            "summaryChars": 129,
            "schemaChars": 374,
            "propertiesCount": 3
          },
          {
            "name": "memory_search",
            "summaryChars": 334,
            "schemaChars": 139,
            "propertiesCount": 3
          },
          {
            "name": "memory_get",
            "summaryChars": 151,
            "schemaChars": 128,
            "propertiesCount": 3
          },
          {
            "name": "feishu_get_user",
            "summaryChars": 75,
            "schemaChars": 185,
            "propertiesCount": 2
          },
          {
            "name": "feishu_search_user",
            "summaryChars": 55,
            "schemaChars": 311,
            "propertiesCount": 3
          },
          {
            "name": "feishu_chat",
            "summaryChars": 92,
            "schemaChars": 519,
            "propertiesCount": 6
          },
          {
            "name": "feishu_chat_members",
            "summaryChars": 54,
            "schemaChars": 353,
            "propertiesCount": 4
          },
          {
            "name": "feishu_im_user_message",
            "summaryChars": 402,
            "schemaChars": 1149,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_user_fetch_resource",
            "summaryChars": 456,
            "schemaChars": 371,
            "propertiesCount": 3
          },
          {
            "name": "feishu_im_user_get_messages",
            "summaryChars": 386,
            "schemaChars": 912,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_user_get_thread_messages",
            "summaryChars": 166,
            "schemaChars": 395,
            "propertiesCount": 4
          },
          {
            "name": "feishu_im_user_search_messages",
            "summaryChars": 522,
            "schemaChars": 1364,
            "propertiesCount": 12
          },
          {
            "name": "feishu_calendar_calendar",
            "summaryChars": 93,
            "schemaChars": 389,
            "propertiesCount": 4
          },
          {
            "name": "feishu_calendar_event",
            "summaryChars": 455,
            "schemaChars": 3200,
            "propertiesCount": 21
          },
          {
            "name": "feishu_calendar_event_attendee",
            "summaryChars": 117,
            "schemaChars": 1129,
            "propertiesCount": 10
          },
          {
            "name": "feishu_calendar_freebusy",
            "summaryChars": 80,
            "schemaChars": 504,
            "propertiesCount": 4
          },
          {
            "name": "feishu_task_task",
            "summaryChars": 167,
            "schemaChars": 1868,
            "propertiesCount": 15
          },
          {
            "name": "feishu_task_tasklist",
            "summaryChars": 199,
            "schemaChars": 795,
            "propertiesCount": 7
          },
          {
            "name": "feishu_task_comment",
            "summaryChars": 95,
            "schemaChars": 671,
            "propertiesCount": 9
          },
          {
            "name": "feishu_task_subtask",
            "summaryChars": 86,
            "schemaChars": 1128,
            "propertiesCount": 9
          },
          {
            "name": "feishu_bitable_app",
            "summaryChars": 139,
            "schemaChars": 511,
            "propertiesCount": 7
          },
          {
            "name": "feishu_bitable_app_table",
            "summaryChars": 320,
            "schemaChars": 1261,
            "propertiesCount": 9
          },
          {
            "name": "feishu_bitable_app_table_record",
            "summaryChars": 292,
            "schemaChars": 2381,
            "propertiesCount": 14
          },
          {
            "name": "feishu_bitable_app_table_field",
            "summaryChars": 134,
            "schemaChars": 824,
            "propertiesCount": 10
          },
          {
            "name": "feishu_bitable_app_table_view",
            "summaryChars": 125,
            "schemaChars": 701,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_bot_image",
            "summaryChars": 241,
            "schemaChars": 384,
            "propertiesCount": 3
          },
          {
            "name": "feishu_oauth",
            "summaryChars": 168,
            "schemaChars": 290,
            "propertiesCount": 1
          },
          {
            "name": "feishu_oauth_batch_auth",
            "summaryChars": 55,
            "schemaChars": 162,
            "propertiesCount": 0
          },
          {
            "name": "wecom_mcp",
            "summaryChars": 288,
            "schemaChars": 426,
            "propertiesCount": 4
          }
        ]
      }
    },
    "totalTokensFresh": false
  },
  "agent:main:session-1774452830525": {
    "sessionId": "c1823431-4af2-420e-8fa4-22483f89cbcc",
    "updatedAt": 1774453622079,
    "systemSent": true,
    "abortedLastRun": false,
    "chatType": "direct",
    "deliveryContext": {
      "channel": "webchat"
    },
    "lastChannel": "webchat",
    "origin": {
      "label": "ClawX",
      "provider": "webchat",
      "surface": "webchat",
      "chatType": "direct"
    },
    "sessionFile": "C:\\Users\\Administrator\\.openclaw\\agents\\main\\sessions\\c1823431-4af2-420e-8fa4-22483f89cbcc.jsonl",
    "compactionCount": 0,
    "skillsSnapshot": {
      "prompt": "\n\nThe following skills provide specialized instructions for specific tasks.\nUse the read tool to load a skill's file when the task matches its description.\nWhen a skill file references a relative path, resolve it against the skill directory (parent of SKILL.md / dirname of the path) and use that absolute path in tool commands.\n\n<available_skills>\n  <skill>\n    <name>feishu-bitable</name>\n    <description>飞书多维表格（Bitable）的创建、查询、编辑和管理工具。包含 27 种字段类型支持、高级筛选、批量操作和视图管理。\n\n**当以下情况时使用此 Skill**：\n(1) 需要创建或管理飞书多维表格 App\n(2) 需要在多维表格中新增、查询、修改、删除记录（行数据）\n(3) 需要管理字段（列）、视图、数据表\n(4) 用户提到&quot;多维表格&quot;、&quot;bitable&quot;、&quot;数据表&quot;、&quot;记录&quot;、&quot;字段&quot;\n(5) 需要批量导入数据或批量更新多维表格\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-bitable\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-calendar</name>\n    <description>飞书日历与日程管理工具集。包含日历管理、日程管理、参会人管理、忙闲查询。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-calendar\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-channel-rules</name>\n    <description>Lark/Feishu channel output rules. Always active in Lark conversations.\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-channel-rules\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-create-doc</name>\n    <description>创建飞书云文档。从 Lark-flavored Markdown 内容创建新的飞书云文档，支持指定创建位置（文件夹/知识库/知识空间）。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-create-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-fetch-doc</name>\n    <description>获取飞书云文档内容。返回文档的 Markdown 内容，支持处理文档中的图片、文件和画板（需配合 feishu_doc_media 工具）。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-fetch-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-im-read</name>\n    <description>飞书 IM 消息读取工具使用指南，覆盖会话消息获取、话题回复读取、跨会话消息搜索、图片/文件资源下载。\n\n**当以下情况时使用此 Skill**:\n(1) 需要获取群聊或单聊的历史消息\n(2) 需要读取话题（thread）内的回复消息\n(3) 需要跨会话搜索消息（按关键词、发送者、时间等条件）\n(4) 消息中包含图片、文件、音频、视频，需要下载\n(5) 用户提到&quot;聊天记录&quot;、&quot;消息&quot;、&quot;群里说了什么&quot;、&quot;话题回复&quot;、&quot;搜索消息&quot;、&quot;图片&quot;、&quot;文件下载&quot;\n(6) 需要按时间范围过滤消息、分页获取更多消息\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-im-read\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-task</name>\n    <description>飞书任务管理工具,用于创建、查询、更新任务和清单。\n\n**当以下情况时使用此 Skill**:\n(1) 需要创建、查询、更新、删除任务\n(2) 需要创建、管理任务清单\n(3) 需要查看任务列表或清单内的任务\n(4) 用户提到&quot;任务&quot;、&quot;待办&quot;、&quot;to-do&quot;、&quot;清单&quot;、&quot;task&quot;\n(5) 需要设置任务负责人、关注人、截止时间\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-task\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-troubleshoot</name>\n    <description>飞书插件问题排查工具。包含常见问题 FAQ 和深度诊断命令（/feishu_doctor）。\n\n常见问题可随时查阅。诊断命令用于排查复杂问题（多次授权仍失败、自动授权无法解决等），\n会检查账户配置、API 连通性、应用权限、用户授权状态，并生成详细的诊断报告和解决方案。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-troubleshoot\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>feishu-update-doc</name>\n    <description>更新飞书云文档。支持 7 种更新模式：追加、覆盖、定位替换、全文替换、前/后插入、删除。\n</description>\n    <location>~/.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-update-doc\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-contact-lookup</name>\n    <description>通讯录成员查询技能，基于 MCP tool 协议封装的 `get_userlist` 接口，获取当前用户可见范围内的通讯录成员，支持按姓名/别名本地筛选匹配。返回 userid、姓名和别名。⚠️ 仅返回当前用户有权限查看的成员，非全量成员。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-contact-lookup\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-doc-manager</name>\n    <description>企业微信文档管理技能。提供文档的创建、读取和编辑能力，支持通过 docid 或文档 URL 操作企业微信文档（doc_type=3）和智能表格（doc_type=10）。适用场景：(1) 以 Markdown 格式导出获取文档完整内容（异步轮询） (2) 新建文档或智能表格 (3) 用 Markdown 格式覆写文档内容。当用户需要查看文档内容、创建新文档、编辑文档正文时触发此 Skill。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-doc-manager\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-edit-todo</name>\n    <description>企业微信待办事项编辑技能，支持创建、更新、删除待办及变更用户处理进度状态。在用户说&quot;帮我创建一个待办&quot;、&quot;把这个任务分派给张三&quot;、&quot;标记待办完成&quot;、&quot;删掉那个待办&quot;、&quot;帮我建个提醒&quot;、&quot;更新一下待办内容&quot;、&quot;把提醒时间改到下周&quot;、&quot;接受这个待办&quot;、&quot;拒绝这个待办&quot;等需要对待办进行写操作的场景时使用。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-edit-todo\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-get-todo-detail</name>\n    <description>企业微信待办详情批量查询技能，根据待办 ID 列表获取完整信息（包含待办内容和分派人）。在用户说&quot;看看这个待办的详情&quot;、&quot;待办内容是什么&quot;、&quot;这个待办分派给谁了&quot;、&quot;告诉我待办的具体信息&quot;等需要查看待办完整内容的场景时使用。通常配合 wecom-get-todo-list 使用——先获取待办 ID 列表，再用本技能获取详情。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-detail\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-get-todo-list</name>\n    <description>企业微信待办列表查询技能，支持按创建时间和提醒时间过滤，支持分页。在用户说&quot;看看我的待办列表&quot;、&quot;我有哪些待办&quot;、&quot;这周的待办有哪些&quot;、&quot;最近有什么待办&quot;、&quot;查一下我的待办&quot;、&quot;列出所有待办&quot;等需要浏览待办概览的场景时使用。注意：此技能仅返回待办概要信息（不含内容和分派人），如需完整详情请配合 wecom-get-todo-detail 使用。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-list\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-meeting-create</name>\n    <description>企业微信会议创建技能, 支持创建预约会议. 当用户需要&quot;创建会议&quot;, &quot;预约会议&quot;, &quot;约会议&quot;, &quot;安排会议&quot;时触发.</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-meeting-create\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-meeting-manage</name>\n    <description>企业微信会议管理技能, 支持取消会议和更新会议受邀成员. 当用户需要&quot;取消会议&quot;, &quot;删除会议&quot;, &quot;修改会议成员&quot;, &quot;添加会议参与人&quot;, &quot;移除会议成员&quot;时触发.</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-meeting-manage\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-meeting-query</name>\n    <description>企业微信会议查询技能, 支持查询会议列表, 获取会议详情, 按关键词查找会议. 当用户需要&quot;查看会议&quot;, &quot;查询会议列表&quot;, &quot;会议详情&quot;, &quot;什么时候开会&quot;, &quot;有哪些会议&quot;, &quot;查找会议&quot;时触发.</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-meeting-query\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-msg</name>\n    <description>企业微信消息技能。提供会话列表查询、消息记录拉取（支持文本/图片/文件/语音/视频）、多媒体文件获取和文本消息发送能力。当用户需要&quot;查看消息&quot;、&quot;看聊天记录&quot;、&quot;发消息给某人&quot;、&quot;最近有什么消息&quot;、&quot;给群里发消息&quot;、&quot;看看发了什么图片/文件&quot;时触发。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-msg\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-preflight</name>\n    <description>企业微信插件前置条件检查。在执行任何 wecom_mcp 操作前，通过 shell 命令检查工具权限配置（profile 和白名单），若缺失则自动修复并提示用户重启 Gateway。所有使用 wecom_mcp 的技能都应在首次调用前执行此检查。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-preflight\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-schedule</name>\n    <description>企业微信日程管理技能。适用于用户对企业微信日程的各类管理需求。当用户需要：(1) 查询指定时间范围内的日程列表或获取日程详细信息（标题、时间、地点、参与者等），(2) 创建新日程并设置提醒、参与人等，(3) 修改已有日程的标题、时间、地点等信息或取消日程，(4) 添加或移除日程参与人，(5) 查询多个成员的闲忙状态并分析共同空闲时段以安排会议时使用此技能。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-schedule\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-smartsheet-data</name>\n    <description>企业微信智能表格数据（记录）管理技能。提供智能表格记录的增删改查能力。适用场景：(1) 查询子表全部记录 (2) 添加一行或多行记录 (3) 更新已有记录 (4) 删除记录。当用户需要读取表格数据、写入新数据、修改或删除表格行时触发此 Skill。支持通过 docid 或文档 URL 定位文档。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-data\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>wecom-smartsheet-schema</name>\n    <description>企业微信智能表格结构管理技能。提供子表（Sheet）和字段（Field/列）的增删改查能力。适用场景：(1) 查询智能表格的子表列表 (2) 添加、更新、删除子表 (3) 查询子表的字段/列信息 (4) 添加、更新、删除字段/列。当用户需要管理智能表格的表结构、列定义、子表配置时触发此 Skill。支持通过 docid 或文档 URL 定位文档。</description>\n    <location>~/.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-schema\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>coding-agent</name>\n    <description>Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. Use when: (1) building/creating new features or apps, (2) reviewing PRs (spawn in temp dir), (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-liner fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat (for example spawn/run Codex or Claude Code in a Discord thread; use sessions_spawn with runtime:&quot;acp&quot;), or any work in ~/clawd workspace (never spawn agents here). Claude Code: use --print --permission-mode bypassPermissions (no PTY). Codex/Pi/OpenCode: pty:true required.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\coding-agent\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>gemini</name>\n    <description>Gemini CLI for one-shot Q&amp;A, summaries, and generation.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\gemini\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>healthcheck</name>\n    <description>Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\healthcheck\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>node-connect</name>\n    <description>Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. Use when QR/setup code/manual connect fails, local Wi-Fi works but VPS/tailnet does not, or errors mention pairing required, unauthorized, bootstrap token invalid or expired, gateway.bind, gateway.remote.url, Tailscale, or plugins.entries.device-pair.config.publicUrl.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\node-connect\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>skill-creator</name>\n    <description>Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch or when asked to improve, review, audit, tidy up, or clean up an existing skill or SKILL.md file. Also use when editing or restructuring a skill directory (moving files to references/ or scripts/, removing stale content, validating against the AgentSkills spec). Triggers on phrases like &quot;create a skill&quot;, &quot;author a skill&quot;, &quot;tidy up a skill&quot;, &quot;improve this skill&quot;, &quot;review the skill&quot;, &quot;clean up the skill&quot;, &quot;audit the skill&quot;.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\skill-creator\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>weather</name>\n    <description>Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed.</description>\n    <location>~/AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\weather\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>ai-video-editing</name>\n    <description>Chat video editor — describe your edit and the AI executes it: trim, cut, merge, add music, color grade, subtitle overlay, and export. Simple video editor with no timeline, no GUI, no learning curve. An easy video editor built for creators who think in ideas, not in keyframes. Supports conversational editing, text-based editing, and natural language video editing for no-timeline video production. Supports mp4, mov, avi, webm, mkv.\n</description>\n    <location>~/.openclaw\\skills\\ai-video-editing-1.0.3\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>automation-workflows</name>\n    <description>Design and implement automation workflows to save time and scale operations as a solopreneur. Use when identifying repetitive tasks to automate, building workflows across tools, setting up triggers and actions, or optimizing existing automations. Covers automation opportunity identification, workflow design, tool selection (Zapier, Make, n8n), testing, and maintenance. Trigger on &quot;automate&quot;, &quot;automation&quot;, &quot;workflow automation&quot;, &quot;save time&quot;, &quot;reduce manual work&quot;, &quot;automate my business&quot;, &quot;no-code automation&quot;.</description>\n    <location>~/.openclaw\\skills\\automation-workflows-0.1.0\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>web-search</name>\n    <description>USE FOR web search. Returns ranked results with snippets, URLs, thumbnails. Supports freshness filters, SafeSearch, Goggles for custom ranking, pagination. Primary search endpoint.</description>\n    <location>~/.openclaw\\skills\\brave-web-search\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>desktop-control</name>\n    <description>Control desktop applications on Windows — launch, close, focus, resize, move windows, simulate keyboard/mouse input, manage processes, control VSCode, read clipboard, and capture screen info. Use when the user wants to interact with any running program, switch windows, type text, press shortcuts, open files in VSCode, manage running processes, or get system display information.</description>\n    <location>~/.openclaw\\skills\\desktop-control-win-1.0.1\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>docx</name>\n    <description>Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of &apos;Word doc&apos;, &apos;word document&apos;, &apos;.docx&apos;, or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a &apos;report&apos;, &apos;memo&apos;, &apos;letter&apos;, &apos;template&apos;, or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.</description>\n    <location>~/.openclaw\\skills\\docx\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>find-skills</name>\n    <description>Helps users discover and install agent skills when they ask questions like &quot;how do I do X&quot;, &quot;find a skill for X&quot;, &quot;is there a skill that can...&quot;, or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.</description>\n    <location>~/.openclaw\\skills\\find-skills\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>pdf</name>\n    <description>Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.</description>\n    <location>~/.openclaw\\skills\\pdf\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>pptx</name>\n    <description>Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions &quot;deck,&quot; &quot;slides,&quot; &quot;presentation,&quot; or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.</description>\n    <location>~/.openclaw\\skills\\pptx\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>self-improvement</name>\n    <description>Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude (&apos;No, that&apos;s wrong...&apos;, &apos;Actually...&apos;), (3) User requests a capability that doesn&apos;t exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks.</description>\n    <location>~/.openclaw\\skills\\self-improving-agent\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>tavily-search</name>\n    <description>Search the web with LLM-optimized results via the Tavily CLI. Use this skill when the user wants to search the web, find articles, look up information, get recent news, discover sources, or says &quot;search for&quot;, &quot;find me&quot;, &quot;look up&quot;, &quot;what&apos;s the latest on&quot;, &quot;find articles about&quot;, or needs current information from the internet. Returns relevant results with content snippets, relevance scores, and metadata — optimized for LLM consumption. Supports domain filtering, time ranges, and multiple search depths.\n</description>\n    <location>~/.openclaw\\skills\\tavily-search\\SKILL.md</location>\n  </skill>\n  <skill>\n    <name>xlsx</name>\n    <description>Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like &quot;the xlsx in my downloads&quot;) — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.</description>\n    <location>~/.openclaw\\skills\\xlsx\\SKILL.md</location>\n  </skill>\n</available_skills>",
      "skills": [
        {
          "name": "feishu-bitable"
        },
        {
          "name": "feishu-calendar"
        },
        {
          "name": "feishu-channel-rules"
        },
        {
          "name": "feishu-create-doc"
        },
        {
          "name": "feishu-fetch-doc"
        },
        {
          "name": "feishu-im-read"
        },
        {
          "name": "feishu-task"
        },
        {
          "name": "feishu-troubleshoot"
        },
        {
          "name": "feishu-update-doc"
        },
        {
          "name": "wecom-contact-lookup"
        },
        {
          "name": "wecom-doc-manager"
        },
        {
          "name": "wecom-edit-todo"
        },
        {
          "name": "wecom-get-todo-detail"
        },
        {
          "name": "wecom-get-todo-list"
        },
        {
          "name": "wecom-meeting-create"
        },
        {
          "name": "wecom-meeting-manage"
        },
        {
          "name": "wecom-meeting-query"
        },
        {
          "name": "wecom-msg"
        },
        {
          "name": "wecom-preflight"
        },
        {
          "name": "wecom-schedule"
        },
        {
          "name": "wecom-smartsheet-data"
        },
        {
          "name": "wecom-smartsheet-schema"
        },
        {
          "name": "coding-agent",
          "requiredEnv": []
        },
        {
          "name": "gemini",
          "requiredEnv": []
        },
        {
          "name": "healthcheck"
        },
        {
          "name": "node-connect"
        },
        {
          "name": "skill-creator"
        },
        {
          "name": "weather",
          "requiredEnv": []
        },
        {
          "name": "ai-video-editing",
          "primaryEnv": "NEMO_TOKEN",
          "requiredEnv": []
        },
        {
          "name": "automation-workflows"
        },
        {
          "name": "web-search"
        },
        {
          "name": "desktop-control"
        },
        {
          "name": "docx"
        },
        {
          "name": "find-skills"
        },
        {
          "name": "pdf"
        },
        {
          "name": "pptx"
        },
        {
          "name": "self-improvement"
        },
        {
          "name": "tavily-search"
        },
        {
          "name": "xlsx"
        }
      ],
      "resolvedSkills": [
        {
          "name": "feishu-bitable",
          "description": "飞书多维表格（Bitable）的创建、查询、编辑和管理工具。包含 27 种字段类型支持、高级筛选、批量操作和视图管理。\n\n**当以下情况时使用此 Skill**：\n(1) 需要创建或管理飞书多维表格 App\n(2) 需要在多维表格中新增、查询、修改、删除记录（行数据）\n(3) 需要管理字段（列）、视图、数据表\n(4) 用户提到\"多维表格\"、\"bitable\"、\"数据表\"、\"记录\"、\"字段\"\n(5) 需要批量导入数据或批量更新多维表格\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-bitable\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-bitable",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-calendar",
          "description": "飞书日历与日程管理工具集。包含日历管理、日程管理、参会人管理、忙闲查询。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-calendar\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-calendar",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-channel-rules",
          "description": "Lark/Feishu channel output rules. Always active in Lark conversations.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-channel-rules\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-channel-rules",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-create-doc",
          "description": "创建飞书云文档。从 Lark-flavored Markdown 内容创建新的飞书云文档，支持指定创建位置（文件夹/知识库/知识空间）。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-create-doc\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-create-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-fetch-doc",
          "description": "获取飞书云文档内容。返回文档的 Markdown 内容，支持处理文档中的图片、文件和画板（需配合 feishu_doc_media 工具）。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-fetch-doc\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-fetch-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-im-read",
          "description": "飞书 IM 消息读取工具使用指南，覆盖会话消息获取、话题回复读取、跨会话消息搜索、图片/文件资源下载。\n\n**当以下情况时使用此 Skill**:\n(1) 需要获取群聊或单聊的历史消息\n(2) 需要读取话题（thread）内的回复消息\n(3) 需要跨会话搜索消息（按关键词、发送者、时间等条件）\n(4) 消息中包含图片、文件、音频、视频，需要下载\n(5) 用户提到\"聊天记录\"、\"消息\"、\"群里说了什么\"、\"话题回复\"、\"搜索消息\"、\"图片\"、\"文件下载\"\n(6) 需要按时间范围过滤消息、分页获取更多消息\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-im-read\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-im-read",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-task",
          "description": "飞书任务管理工具,用于创建、查询、更新任务和清单。\n\n**当以下情况时使用此 Skill**:\n(1) 需要创建、查询、更新、删除任务\n(2) 需要创建、管理任务清单\n(3) 需要查看任务列表或清单内的任务\n(4) 用户提到\"任务\"、\"待办\"、\"to-do\"、\"清单\"、\"task\"\n(5) 需要设置任务负责人、关注人、截止时间\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-task\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-task",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-troubleshoot",
          "description": "飞书插件问题排查工具。包含常见问题 FAQ 和深度诊断命令（/feishu_doctor）。\n\n常见问题可随时查阅。诊断命令用于排查复杂问题（多次授权仍失败、自动授权无法解决等），\n会检查账户配置、API 连通性、应用权限、用户授权状态，并生成详细的诊断报告和解决方案。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-troubleshoot\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-troubleshoot",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "feishu-update-doc",
          "description": "更新飞书云文档。支持 7 种更新模式：追加、覆盖、定位替换、全文替换、前/后插入、删除。\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-update-doc\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\feishu-openclaw-plugin\\skills\\feishu-update-doc",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-contact-lookup",
          "description": "通讯录成员查询技能，基于 MCP tool 协议封装的 `get_userlist` 接口，获取当前用户可见范围内的通讯录成员，支持按姓名/别名本地筛选匹配。返回 userid、姓名和别名。⚠️ 仅返回当前用户有权限查看的成员，非全量成员。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-contact-lookup\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-contact-lookup",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-doc-manager",
          "description": "企业微信文档管理技能。提供文档的创建、读取和编辑能力，支持通过 docid 或文档 URL 操作企业微信文档（doc_type=3）和智能表格（doc_type=10）。适用场景：(1) 以 Markdown 格式导出获取文档完整内容（异步轮询） (2) 新建文档或智能表格 (3) 用 Markdown 格式覆写文档内容。当用户需要查看文档内容、创建新文档、编辑文档正文时触发此 Skill。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-doc-manager\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-doc-manager",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-edit-todo",
          "description": "企业微信待办事项编辑技能，支持创建、更新、删除待办及变更用户处理进度状态。在用户说\"帮我创建一个待办\"、\"把这个任务分派给张三\"、\"标记待办完成\"、\"删掉那个待办\"、\"帮我建个提醒\"、\"更新一下待办内容\"、\"把提醒时间改到下周\"、\"接受这个待办\"、\"拒绝这个待办\"等需要对待办进行写操作的场景时使用。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-edit-todo\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-edit-todo",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-get-todo-detail",
          "description": "企业微信待办详情批量查询技能，根据待办 ID 列表获取完整信息（包含待办内容和分派人）。在用户说\"看看这个待办的详情\"、\"待办内容是什么\"、\"这个待办分派给谁了\"、\"告诉我待办的具体信息\"等需要查看待办完整内容的场景时使用。通常配合 wecom-get-todo-list 使用——先获取待办 ID 列表，再用本技能获取详情。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-detail\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-detail",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-get-todo-list",
          "description": "企业微信待办列表查询技能，支持按创建时间和提醒时间过滤，支持分页。在用户说\"看看我的待办列表\"、\"我有哪些待办\"、\"这周的待办有哪些\"、\"最近有什么待办\"、\"查一下我的待办\"、\"列出所有待办\"等需要浏览待办概览的场景时使用。注意：此技能仅返回待办概要信息（不含内容和分派人），如需完整详情请配合 wecom-get-todo-detail 使用。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-list\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-get-todo-list",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-meeting-create",
          "description": "企业微信会议创建技能, 支持创建预约会议. 当用户需要\"创建会议\", \"预约会议\", \"约会议\", \"安排会议\"时触发.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-create\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-create",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-meeting-manage",
          "description": "企业微信会议管理技能, 支持取消会议和更新会议受邀成员. 当用户需要\"取消会议\", \"删除会议\", \"修改会议成员\", \"添加会议参与人\", \"移除会议成员\"时触发.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-manage\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-manage",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-meeting-query",
          "description": "企业微信会议查询技能, 支持查询会议列表, 获取会议详情, 按关键词查找会议. 当用户需要\"查看会议\", \"查询会议列表\", \"会议详情\", \"什么时候开会\", \"有哪些会议\", \"查找会议\"时触发.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-query\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-meeting-query",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-msg",
          "description": "企业微信消息技能。提供会话列表查询、消息记录拉取（支持文本/图片/文件/语音/视频）、多媒体文件获取和文本消息发送能力。当用户需要\"查看消息\"、\"看聊天记录\"、\"发消息给某人\"、\"最近有什么消息\"、\"给群里发消息\"、\"看看发了什么图片/文件\"时触发。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-msg\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-msg",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-preflight",
          "description": "企业微信插件前置条件检查。在执行任何 wecom_mcp 操作前，通过 shell 命令检查工具权限配置（profile 和白名单），若缺失则自动修复并提示用户重启 Gateway。所有使用 wecom_mcp 的技能都应在首次调用前执行此检查。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-preflight\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-preflight",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-schedule",
          "description": "企业微信日程管理技能。适用于用户对企业微信日程的各类管理需求。当用户需要：(1) 查询指定时间范围内的日程列表或获取日程详细信息（标题、时间、地点、参与者等），(2) 创建新日程并设置提醒、参与人等，(3) 修改已有日程的标题、时间、地点等信息或取消日程，(4) 添加或移除日程参与人，(5) 查询多个成员的闲忙状态并分析共同空闲时段以安排会议时使用此技能。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-schedule\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-schedule",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-smartsheet-data",
          "description": "企业微信智能表格数据（记录）管理技能。提供智能表格记录的增删改查能力。适用场景：(1) 查询子表全部记录 (2) 添加一行或多行记录 (3) 更新已有记录 (4) 删除记录。当用户需要读取表格数据、写入新数据、修改或删除表格行时触发此 Skill。支持通过 docid 或文档 URL 定位文档。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-data\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-data",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "wecom-smartsheet-schema",
          "description": "企业微信智能表格结构管理技能。提供子表（Sheet）和字段（Field/列）的增删改查能力。适用场景：(1) 查询智能表格的子表列表 (2) 添加、更新、删除子表 (3) 查询子表的字段/列信息 (4) 添加、更新、删除字段/列。当用户需要管理智能表格的表结构、列定义、子表配置时触发此 Skill。支持通过 docid 或文档 URL 定位文档。",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-schema\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\extensions\\wecom\\skills\\wecom-smartsheet-schema",
          "source": "openclaw-extra",
          "disableModelInvocation": false
        },
        {
          "name": "coding-agent",
          "description": "Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. Use when: (1) building/creating new features or apps, (2) reviewing PRs (spawn in temp dir), (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-liner fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat (for example spawn/run Codex or Claude Code in a Discord thread; use sessions_spawn with runtime:\"acp\"), or any work in ~/clawd workspace (never spawn agents here). Claude Code: use --print --permission-mode bypassPermissions (no PTY). Codex/Pi/OpenCode: pty:true required.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\coding-agent\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\coding-agent",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "gemini",
          "description": "Gemini CLI for one-shot Q&A, summaries, and generation.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\gemini\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\gemini",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "healthcheck",
          "description": "Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\healthcheck\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\healthcheck",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "node-connect",
          "description": "Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. Use when QR/setup code/manual connect fails, local Wi-Fi works but VPS/tailnet does not, or errors mention pairing required, unauthorized, bootstrap token invalid or expired, gateway.bind, gateway.remote.url, Tailscale, or plugins.entries.device-pair.config.publicUrl.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\node-connect\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\node-connect",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "skill-creator",
          "description": "Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch or when asked to improve, review, audit, tidy up, or clean up an existing skill or SKILL.md file. Also use when editing or restructuring a skill directory (moving files to references/ or scripts/, removing stale content, validating against the AgentSkills spec). Triggers on phrases like \"create a skill\", \"author a skill\", \"tidy up a skill\", \"improve this skill\", \"review the skill\", \"clean up the skill\", \"audit the skill\".",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\skill-creator\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\skill-creator",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "weather",
          "description": "Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed.",
          "filePath": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\weather\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\ClawX\\resources\\openclaw\\skills\\weather",
          "source": "openclaw-bundled",
          "disableModelInvocation": false
        },
        {
          "name": "ai-video-editing",
          "description": "Chat video editor — describe your edit and the AI executes it: trim, cut, merge, add music, color grade, subtitle overlay, and export. Simple video editor with no timeline, no GUI, no learning curve. An easy video editor built for creators who think in ideas, not in keyframes. Supports conversational editing, text-based editing, and natural language video editing for no-timeline video production. Supports mp4, mov, avi, webm, mkv.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\ai-video-editing-1.0.3\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\ai-video-editing-1.0.3",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "automation-workflows",
          "description": "Design and implement automation workflows to save time and scale operations as a solopreneur. Use when identifying repetitive tasks to automate, building workflows across tools, setting up triggers and actions, or optimizing existing automations. Covers automation opportunity identification, workflow design, tool selection (Zapier, Make, n8n), testing, and maintenance. Trigger on \"automate\", \"automation\", \"workflow automation\", \"save time\", \"reduce manual work\", \"automate my business\", \"no-code automation\".",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\automation-workflows-0.1.0\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\automation-workflows-0.1.0",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "web-search",
          "description": "USE FOR web search. Returns ranked results with snippets, URLs, thumbnails. Supports freshness filters, SafeSearch, Goggles for custom ranking, pagination. Primary search endpoint.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\brave-web-search\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\brave-web-search",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "desktop-control",
          "description": "Control desktop applications on Windows — launch, close, focus, resize, move windows, simulate keyboard/mouse input, manage processes, control VSCode, read clipboard, and capture screen info. Use when the user wants to interact with any running program, switch windows, type text, press shortcuts, open files in VSCode, manage running processes, or get system display information.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\desktop-control-win-1.0.1\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\desktop-control-win-1.0.1",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "docx",
          "description": "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\docx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\docx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "find-skills",
          "description": "Helps users discover and install agent skills when they ask questions like \"how do I do X\", \"find a skill for X\", \"is there a skill that can...\", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\find-skills\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\find-skills",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "pdf",
          "description": "Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\pdf\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\pdf",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "pptx",
          "description": "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\pptx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\pptx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "self-improvement",
          "description": "Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\self-improving-agent\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\self-improving-agent",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "tavily-search",
          "description": "Search the web with LLM-optimized results via the Tavily CLI. Use this skill when the user wants to search the web, find articles, look up information, get recent news, discover sources, or says \"search for\", \"find me\", \"look up\", \"what's the latest on\", \"find articles about\", or needs current information from the internet. Returns relevant results with content snippets, relevance scores, and metadata — optimized for LLM consumption. Supports domain filtering, time ranges, and multiple search depths.\n",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\tavily-search\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\tavily-search",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        },
        {
          "name": "xlsx",
          "description": "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.",
          "filePath": "C:\\Users\\Administrator\\.openclaw\\skills\\xlsx\\SKILL.md",
          "baseDir": "C:\\Users\\Administrator\\.openclaw\\skills\\xlsx",
          "source": "openclaw-managed",
          "disableModelInvocation": false
        }
      ],
      "version": 0
    },
    "authProfileOverride": "ollama-ollamacb:default",
    "authProfileOverrideSource": "auto",
    "authProfileOverrideCompactionCount": 0,
    "modelProvider": "ollama-ollamacb",
    "model": "qwen3.5:2b",
    "contextTokens": 200000,
    "systemPromptReport": {
      "source": "run",
      "generatedAt": 1774453452049,
      "sessionId": "c1823431-4af2-420e-8fa4-22483f89cbcc",
      "sessionKey": "agent:main:session-1774452830525",
      "provider": "ollama-ollamacb",
      "model": "qwen3.5:2b",
      "workspaceDir": "C:\\Users\\Administrator\\.openclaw\\workspace",
      "bootstrapMaxChars": 20000,
      "bootstrapTotalMaxChars": 150000,
      "bootstrapTruncation": {
        "warningMode": "once",
        "warningShown": false,
        "truncatedFiles": 0,
        "nearLimitFiles": 0,
        "totalNearLimit": false
      },
      "sandbox": {
        "mode": "off",
        "sandboxed": false
      },
      "systemPrompt": {
        "chars": 51140,
        "projectContextChars": 14516,
        "nonProjectContextChars": 36624
      },
      "injectedWorkspaceFiles": [
        {
          "name": "AGENTS.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\AGENTS.md",
          "missing": false,
          "rawChars": 8018,
          "injectedChars": 8018,
          "truncated": false
        },
        {
          "name": "SOUL.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\SOUL.md",
          "missing": false,
          "rawChars": 1664,
          "injectedChars": 1664,
          "truncated": false
        },
        {
          "name": "TOOLS.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\TOOLS.md",
          "missing": false,
          "rawChars": 1486,
          "injectedChars": 1486,
          "truncated": false
        },
        {
          "name": "IDENTITY.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\IDENTITY.md",
          "missing": false,
          "rawChars": 633,
          "injectedChars": 633,
          "truncated": false
        },
        {
          "name": "USER.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\USER.md",
          "missing": false,
          "rawChars": 474,
          "injectedChars": 474,
          "truncated": false
        },
        {
          "name": "HEARTBEAT.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\HEARTBEAT.md",
          "missing": false,
          "rawChars": 167,
          "injectedChars": 167,
          "truncated": false
        },
        {
          "name": "BOOTSTRAP.md",
          "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\BOOTSTRAP.md",
          "missing": false,
          "rawChars": 1449,
          "injectedChars": 1449,
          "truncated": false
        }
      ],
      "skills": {
        "promptChars": 18711,
        "entries": [
          {
            "name": "feishu-bitable",
            "blockChars": 453
          },
          {
            "name": "feishu-calendar",
            "blockChars": 223
          },
          {
            "name": "feishu-channel-rules",
            "blockChars": 267
          },
          {
            "name": "feishu-create-doc",
            "blockChars": 259
          },
          {
            "name": "feishu-fetch-doc",
            "blockChars": 259
          },
          {
            "name": "feishu-im-read",
            "blockChars": 508
          },
          {
            "name": "feishu-task",
            "blockChars": 393
          },
          {
            "name": "feishu-troubleshoot",
            "blockChars": 330
          },
          {
            "name": "feishu-update-doc",
            "blockChars": 235
          },
          {
            "name": "wecom-contact-lookup",
            "blockChars": 299
          },
          {
            "name": "wecom-doc-manager",
            "blockChars": 370
          },
          {
            "name": "wecom-edit-todo",
            "blockChars": 409
          },
          {
            "name": "wecom-get-todo-detail",
            "blockChars": 384
          },
          {
            "name": "wecom-get-todo-list",
            "blockChars": 410
          },
          {
            "name": "wecom-meeting-create",
            "blockChars": 279
          },
          {
            "name": "wecom-meeting-manage",
            "blockChars": 312
          },
          {
            "name": "wecom-meeting-query",
            "blockChars": 337
          },
          {
            "name": "wecom-msg",
            "blockChars": 342
          },
          {
            "name": "wecom-preflight",
            "blockChars": 292
          },
          {
            "name": "wecom-schedule",
            "blockChars": 346
          },
          {
            "name": "wecom-smartsheet-data",
            "blockChars": 329
          },
          {
            "name": "wecom-smartsheet-schema",
            "blockChars": 359
          },
          {
            "name": "coding-agent",
            "blockChars": 842
          },
          {
            "name": "gemini",
            "blockChars": 231
          },
          {
            "name": "healthcheck",
            "blockChars": 501
          },
          {
            "name": "node-connect",
            "blockChars": 551
          },
          {
            "name": "skill-creator",
            "blockChars": 769
          },
          {
            "name": "weather",
            "blockChars": 426
          },
          {
            "name": "ai-video-editing",
            "blockChars": 595
          },
          {
            "name": "automation-workflows",
            "blockChars": 750
          },
          {
            "name": "web-search",
            "blockChars": 328
          },
          {
            "name": "desktop-control",
            "blockChars": 542
          },
          {
            "name": "docx",
            "blockChars": 985
          },
          {
            "name": "find-skills",
            "blockChars": 477
          },
          {
            "name": "pdf",
            "blockChars": 565
          },
          {
            "name": "pptx",
            "blockChars": 848
          },
          {
            "name": "self-improvement",
            "blockChars": 633
          },
          {
            "name": "tavily-search",
            "blockChars": 709
          },
          {
            "name": "xlsx",
            "blockChars": 1081
          }
        ]
      },
      "tools": {
        "listChars": 8418,
        "schemaChars": 40979,
        "entries": [
          {
            "name": "read",
            "summaryChars": 298,
            "schemaChars": 392,
            "propertiesCount": 4
          },
          {
            "name": "edit",
            "summaryChars": 129,
            "schemaChars": 591,
            "propertiesCount": 6
          },
          {
            "name": "write",
            "summaryChars": 127,
            "schemaChars": 313,
            "propertiesCount": 3
          },
          {
            "name": "exec",
            "summaryChars": 181,
            "schemaChars": 1086,
            "propertiesCount": 12
          },
          {
            "name": "process",
            "summaryChars": 85,
            "schemaChars": 961,
            "propertiesCount": 12
          },
          {
            "name": "browser",
            "summaryChars": 1683,
            "schemaChars": 2799,
            "propertiesCount": 48
          },
          {
            "name": "canvas",
            "summaryChars": 106,
            "schemaChars": 661,
            "propertiesCount": 18
          },
          {
            "name": "nodes",
            "summaryChars": 122,
            "schemaChars": 1800,
            "propertiesCount": 37
          },
          {
            "name": "cron",
            "summaryChars": 2689,
            "schemaChars": 690,
            "propertiesCount": 13
          },
          {
            "name": "message",
            "summaryChars": 89,
            "schemaChars": 4860,
            "propertiesCount": 91
          },
          {
            "name": "tts",
            "summaryChars": 152,
            "schemaChars": 223,
            "propertiesCount": 2
          },
          {
            "name": "gateway",
            "summaryChars": 464,
            "schemaChars": 497,
            "propertiesCount": 12
          },
          {
            "name": "agents_list",
            "summaryChars": 118,
            "schemaChars": 33,
            "propertiesCount": 0
          },
          {
            "name": "sessions_list",
            "summaryChars": 54,
            "schemaChars": 212,
            "propertiesCount": 4
          },
          {
            "name": "sessions_history",
            "summaryChars": 36,
            "schemaChars": 161,
            "propertiesCount": 3
          },
          {
            "name": "sessions_send",
            "summaryChars": 84,
            "schemaChars": 273,
            "propertiesCount": 5
          },
          {
            "name": "sessions_yield",
            "summaryChars": 97,
            "schemaChars": 60,
            "propertiesCount": 1
          },
          {
            "name": "sessions_spawn",
            "summaryChars": 198,
            "schemaChars": 1179,
            "propertiesCount": 17
          },
          {
            "name": "subagents",
            "summaryChars": 105,
            "schemaChars": 191,
            "propertiesCount": 4
          },
          {
            "name": "session_status",
            "summaryChars": 207,
            "schemaChars": 89,
            "propertiesCount": 2
          },
          {
            "name": "web_search",
            "summaryChars": 175,
            "schemaChars": 1084,
            "propertiesCount": 9
          },
          {
            "name": "web_fetch",
            "summaryChars": 129,
            "schemaChars": 374,
            "propertiesCount": 3
          },
          {
            "name": "memory_search",
            "summaryChars": 334,
            "schemaChars": 139,
            "propertiesCount": 3
          },
          {
            "name": "memory_get",
            "summaryChars": 151,
            "schemaChars": 128,
            "propertiesCount": 3
          },
          {
            "name": "feishu_get_user",
            "summaryChars": 75,
            "schemaChars": 185,
            "propertiesCount": 2
          },
          {
            "name": "feishu_search_user",
            "summaryChars": 55,
            "schemaChars": 311,
            "propertiesCount": 3
          },
          {
            "name": "feishu_chat",
            "summaryChars": 92,
            "schemaChars": 519,
            "propertiesCount": 6
          },
          {
            "name": "feishu_chat_members",
            "summaryChars": 54,
            "schemaChars": 353,
            "propertiesCount": 4
          },
          {
            "name": "feishu_im_user_message",
            "summaryChars": 402,
            "schemaChars": 1149,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_user_fetch_resource",
            "summaryChars": 456,
            "schemaChars": 371,
            "propertiesCount": 3
          },
          {
            "name": "feishu_im_user_get_messages",
            "summaryChars": 386,
            "schemaChars": 912,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_user_get_thread_messages",
            "summaryChars": 166,
            "schemaChars": 395,
            "propertiesCount": 4
          },
          {
            "name": "feishu_im_user_search_messages",
            "summaryChars": 522,
            "schemaChars": 1364,
            "propertiesCount": 12
          },
          {
            "name": "feishu_calendar_calendar",
            "summaryChars": 93,
            "schemaChars": 389,
            "propertiesCount": 4
          },
          {
            "name": "feishu_calendar_event",
            "summaryChars": 455,
            "schemaChars": 3200,
            "propertiesCount": 21
          },
          {
            "name": "feishu_calendar_event_attendee",
            "summaryChars": 117,
            "schemaChars": 1129,
            "propertiesCount": 10
          },
          {
            "name": "feishu_calendar_freebusy",
            "summaryChars": 80,
            "schemaChars": 504,
            "propertiesCount": 4
          },
          {
            "name": "feishu_task_task",
            "summaryChars": 167,
            "schemaChars": 1868,
            "propertiesCount": 15
          },
          {
            "name": "feishu_task_tasklist",
            "summaryChars": 199,
            "schemaChars": 795,
            "propertiesCount": 7
          },
          {
            "name": "feishu_task_comment",
            "summaryChars": 95,
            "schemaChars": 671,
            "propertiesCount": 9
          },
          {
            "name": "feishu_task_subtask",
            "summaryChars": 86,
            "schemaChars": 1128,
            "propertiesCount": 9
          },
          {
            "name": "feishu_bitable_app",
            "summaryChars": 139,
            "schemaChars": 511,
            "propertiesCount": 7
          },
          {
            "name": "feishu_bitable_app_table",
            "summaryChars": 320,
            "schemaChars": 1261,
            "propertiesCount": 9
          },
          {
            "name": "feishu_bitable_app_table_record",
            "summaryChars": 292,
            "schemaChars": 2381,
            "propertiesCount": 14
          },
          {
            "name": "feishu_bitable_app_table_field",
            "summaryChars": 134,
            "schemaChars": 824,
            "propertiesCount": 10
          },
          {
            "name": "feishu_bitable_app_table_view",
            "summaryChars": 125,
            "schemaChars": 701,
            "propertiesCount": 8
          },
          {
            "name": "feishu_im_bot_image",
            "summaryChars": 241,
            "schemaChars": 384,
            "propertiesCount": 3
          },
          {
            "name": "feishu_oauth",
            "summaryChars": 168,
            "schemaChars": 290,
            "propertiesCount": 1
          },
          {
            "name": "feishu_oauth_batch_auth",
            "summaryChars": 55,
            "schemaChars": 162,
            "propertiesCount": 0
          },
          {
            "name": "wecom_mcp",
            "summaryChars": 288,
            "schemaChars": 426,
            "propertiesCount": 4
          }
        ]
      }
    },
    "totalTokensFresh": false
  }
}
```
