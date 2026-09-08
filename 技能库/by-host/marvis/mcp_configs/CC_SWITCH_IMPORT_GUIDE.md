# CC Switch 逐个导入指南

## 通用操作步骤

1. 点击右上角 **"添加MCP"**
2. 类型选择 **"自定义"**
3. 填写 **MCP标题**（唯一标识符）
4. 按需勾选 **启用到应用**（建议 Claude + Codex + Gemini 全勾）
5. 在底部 **"完整的JSON配置"** 区域粘贴对应的 JSON
6. 点击右下角 **"+ 添加"**

---

## 1. 网页搜索 (Brave)

| 字段 | 值 |
|------|-----|
| MCP标题 | `lobster_web_search_v1` |
| 显示名称 | `@modelcontextprotocol/server-brave-search` |
| 启用到应用 | Claude, Codex, Gemini |

**JSON配置：**
```json
{"type": "stdio", "command": "npx", "args": ["-y", "@modelcontextprotocol/server-brave-search"], "env": {"BRAVE_API_KEY": "BSA3FhC6CtBc292TTVb3wq3pPAc6v4h"}}
```

---

## 2. 网盘搜索 (夸克/百度/阿里)

| 字段 | 值 |
|------|-----|
| MCP标题 | `lobster_netdisk_search_v1` |
| 显示名称 | `lobster-netdisk-search` |
| 启用到应用 | Claude, Codex, Gemini |

**JSON配置：**
```json
{"type": "stdio", "command": "node", "args": ["C:\\Users\\Administrator\\.workbuddy\\mcp-servers\\lobster-netdisk-search\\index.js"], "env": {"QUARK_COOKIE": "AGL_USER_ID=c01a6c7b-3839-430e-93ee-91b9427136e3; __itrace_wid=bf2dfe38-cf2e-4bec-10ef-90e792ac617f; __wpkreporterwid_=a7adea49-3d03-4dd3-a628-4fe1f620ad67; b-user-id=b71645d6-9f31-a0bd-1796-9ec589e8ffc6; __wpkreporterwid_=8b142b84-6a94-4f3a-39f9-897a6603542d; b-user-id=842500e8-5b97-38d7-2bbd-649ce59078d0", "BAIDU_COOKIE": "BDUSS=praFc0ejVQTTB4VU9kd2NaNVZmdExwZlVac2hsfnE3OWF-WnRyWThwd0xWeGhwRVFBQUFBJCQAAAAAAAAAAAEAAAAA5k9BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAvK8GgLyvBod1; BIDUPSID=2A51F20CCDA41CF8EC10C355D1AE434F; PSTM=1774283301; ZFY=J5EwL9svdPebBXw0tatLFQsDvrZi6cvXElKDFnIhuaI:C; BA_HECTOR=040g81a58h8l0100200kag2l810g0l1kvpvpp27; BAIDUID_BFESS=2A51F20CCDA41CF8EC10C355D1AE434F:FG=1; BDUSS_BFESS=praFc0ejVQTTB4VU9kd2NaNVZmdExwZlVac2hsfnE3OWF-WnRyWThwd0xWeGhwRVFBQUFBJCQAAAAAAAAAAAEAAAAA5k9BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAvK8GgLyvBod1; H_PS_PSSID=63144_67603_67861_68165_68296_68742_69005_69061_69165_69182_69201_69226_69245_69241_69231_69237_69290_69296_69250_69373_69383_69403_69396_69420_69416_69414_69423_69440_69432_69454_69343_69339_69347_69345_69348_69351_69340_69502_69514_69553_69574_69593_69613_69653_69665_69666_69661_69741_69726_69761_69767_69798_69778_69712_69808_69833; H_WISE_SIDS=63144_67603_67861_68165_68296_68742_69005_69061_69165_69182_69201_69226_69245_69241_69231_69237_69290_69296_69250_69373_69383_69403_69396_69420_69416_69414_69423_69440_69432_69454_69343_69339_69347_69345_69348_69351_69340_69502_69514_69553_69574_69593_69613_69653_69665_69666_69661_69741_69726_69761_69767_69798_69778_69712_69808_69833; HMACCOUNT=FFC843BD0430EFA5; HMACCOUNT_BFESS=FFC843BD0430EFA5; STOKEN=ce9a80148eda3c933a9f23a36e6c584b67ccbc3477161126d68e76e8c7927f55; ab_bid=32624d36acefaca4ec26dc3b4be6471f9008; ab_jid=32624d36acefaca4ec26dc3b4be6471f9008; ab_jid_BFESS=32624d36acefaca4ec26dc3b4be6471f9008; BD_UPN=12314753", "ALIYUN_REFRESH_TOKEN": "fa5a9aa2ca2547f308eb44e5d70974doc"}}
```

---

## 3. 小红书 (Playwright)

| 字段 | 值 |
|------|-----|
| MCP标题 | `lobster_xiaohongshu_v1` |
| 显示名称 | `playwright-mcp-xiaohongshu` |
| 启用到应用 | Claude, Codex, Gemini |

**JSON配置：**
```json
{"type": "stdio", "command": "npx", "args": ["-y", "playwright-mcp", "--browser", "msedge"], "env": {"PLAYWRIGHT_BROWSER": "msedge", "PLAYWRIGHT_EXECUTABLE_PATH": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "XHS_COOKIE": "a1=19e4ff1d973ilhxid2gjjh3i2t391787sap6xidf450000654125; sec_poison_id=a84432c0-8d6a-4f49-9baf-c9b3d9b34aab; webId=fdd433253f93d1a2bd6f8b2b17b85d8e; websectiga=f47eda31ec99545da40c2f731f0630efd2b0959e1dd10d5fedac3dce0bd1e04d; gid=yjd4iiydiKMqyjd4iiyfj03fWq31xC3fJkVVUi4xq3J9qK28jyWYWC888K24yJ284WKq8dj8; xsecappid=adsportal; acw_tc=0a0d003a17794577123051873e3f35451e1554d3072a74142b3ee39b2c398f; ads-portal_worker_plugin_uuid=b06d1405654b470897bf8138138d0fca; token=%7B%22accessToken%22%3A%22eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNzE3MjI2IiwiZXhwIjoxNzc5NjMwNTY2fQ.M2HC51AMynqt8zjll4sUOjK0SFyYj7euvpSayTn3lLc%22%2C%22expiredIn%22%3A172800000%2C%22refreshToken%22%3A%22eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNzE3MjI2In0.sugSn7wxnydKus82jar1i2p1afOmF-1vtmHvzSSIQRE%22%2C%22mktClueId%22%3Anull%7D; acw_tc=0a0bb04217794577129656987e0027ac046332a4d636d633f5ac918034f5ca; acw_tc=0a00d79717794577129123971e79a359c8b033a7647ce452f1e938d4dc35fe"}}
```

---

## 4. 微信视频号 (Playwright)

| 字段 | 值 |
|------|-----|
| MCP标题 | `lobster_wechat_video_v1` |
| 显示名称 | `playwright-mcp-wechat-video` |
| 启用到应用 | Claude, Codex, Gemini |

**JSON配置：**
```json
{"type": "stdio", "command": "npx", "args": ["-y", "playwright-mcp", "--browser", "msedge"], "env": {"PLAYWRIGHT_BROWSER": "msedge", "PLAYWRIGHT_EXECUTABLE_PATH": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "PLAYWRIGHT_HEADLESS": "false", "WECHAT_VIDEO_COOKIE": "sessionid=BgAATacYT%2F2NfKl9SKyv5Cccqas42I2YCapeICBhgW8Z5YnK51EHg5b6PgJUlljp76xm19Dv+fT4Ejm7hOZ0%2FM039ABTgX71Mxhk1dDXMP15Q3; wxuin=2288170887"}}
```

---

## 5. 桌面自动化 (Puppeteer)

| 字段 | 值 |
|------|-----|
| MCP标题 | `lobster_desktop_automation_v1` |
| 显示名称 | `@modelcontextprotocol/server-puppeteer` |
| 启用到应用 | Claude, Codex, Gemini |

**JSON配置：**
```json
{"type": "stdio", "command": "npx", "args": ["-y", "@modelcontextprotocol/server-puppeteer"], "env": {"PUPPETEER_EXECUTABLE_PATH": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "PUPPETEER_HEADLESS": "false", "PUPPETEER_BROWSER": "msedge"}}
```

---

## 汇总

| # | MCP标题 | 类型 | 依赖 |
|---|---------|------|------|
| 1 | `lobster_web_search_v1` | npx自动下载 | 无需预装 |
| 2 | `lobster_netdisk_search_v1` | node本地脚本 | 脚本已就绪 |
| 3 | `lobster_xiaohongshu_v1` | npx自动下载 | playwright-mcp |
| 4 | `lobster_wechat_video_v1` | npx自动下载 | playwright-mcp |
| 5 | `lobster_desktop_automation_v1` | npx自动下载 | puppeteer |

**导入完成后：** CC Switch 将显示 **14个服务器**（原有9个 + 新增5个）
