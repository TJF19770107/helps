---
name: "external_mcp_catalog_from_screenshot_v1.0"
description: "MCP 技能清单（按本次对话中用户截图文字原样登记）：仅做右侧可见注册与清单留存，不等同于已安装/已启用对应 MCP Server。"
---

# MCP 技能清单（原样登记）

本技能只负责把你提供的 MCP 包名清单在 Trae 右侧全局技能列表中显性展示与可检索留存；不对 MCP Server 的实际安装与鉴权状态做任何虚假承诺。

【1. 开发类（6个）】
1. Filesystem：读写本地文件、列目录、改内容；包名：server-filesystem
2. Git：提交、diff、log、切分支；包名：server-git
3. GitHub：建仓、提PR、读Issue；包名：server-github（需Token）
4. Shell/Terminal：执行命令、跑脚本、看输出；包名：mcp-server-shell
5. Docker：看容器、起服务、读日志；包名：mcp-server-docker
6. Code Runner：沙箱跑Python/JS/Bash；包名：mcp-code-runner

【2. 数据类（5个）】
1. SQLite：本地零配置SQL读写；包名：server-sqlite
2. Postgres：连数据库做查询、改表；包名：server-postgres
3. MySQL：兼容MySQL/MariaDB；包名：mcp-server-mysql
4. Redis：KV缓存、队列、发布订阅；包名：mcp-server-redis
5. Memory（向量记忆）：给AI加长期跨会话记忆；包名：server-memory

【3. 浏览器与抓取类（5个）】
1. Playwright：操控真浏览器、截图；包名：server-playwright
2. Puppeteer：无头浏览器、抓JS渲染页；包名：mcp-puppeteer
3. Browser Use：语义级浏览器代理；包名：mcp-browser-use
4. Fetch：抓URL转Markdown给AI读；包名：server-fetch
5. Firecrawl：整站爬取、结构化；包名：mcp-firecrawl（免费额度）

【4. 文件与办公类（5个）】
1. PDF Reader：读PDF、提文本、查关键词；包名：mcp-pdf-reader
2. Excel/Sheets：读写表格、跑公式；包名：mcp-excel
3. Word/Docs：读写docx、改样式；包名：mcp-word
4. Obsidian：操作本地知识库.md；包名：mcp-obsidian
5. Notion：建页/改库/查内容；包名：server-notion（需Key）

【5. 通讯与协作类（4个）】
1. Slack：发消息、查频道、@人；包名：server-slack（需Token）
2. Discord：机器人发言、读频道；包名：mcp-discord（需Token）
3. Email (IMAP)：读邮件、搜邮件、回邮件；包名：mcp-email
4. Google Calendar：看日程、建日程、提醒；包名：mcp-gcal（需OAuth）

【6. 生活效率类（5个）】
1. Google Maps：查地点、算路线、看营业；包名：mcp-gmaps（需Key）
2. Weather：当前+预报+预警；包名：mcp-weather
3. Time：时区换算、定时任务；包名：mcp-time
4. Web Search：实时联网搜索（Brave/SearxNG）；包名：mcp-search
5. YouTube：搜视频、读字幕、做摘要；包名：mcp-youtube
