# gateway.log

```
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 4ms
[GatewayManager] Startup phase: sanitize openclaw config took 10ms
[GatewayManager] Startup phase: validate and fix config skipped for version 0.2.26 on packaged Windows first launch/update
[GatewayManager] Startup phase: ensure builtin skills took 494ms
[GatewayManager] Startup phase: ensure skill path guidance took 0ms
[GatewayManager] Startup phase: pre-register device took 4ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 514ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 239ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 527ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 2ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 1ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 141ms
[GatewayManager] Startup phase: patch gateway runtime took 1505ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
2026-04-14T02:35:10.048+08:00 [gateway] force: no listeners on port 18789
2026-04-14T02:35:10.096+08:00 [gateway] [plugins] memory slot plugin not found or not marked as memory: memory-core
2026-04-14T02:35:10.112+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T02:35:10.250+08:00 [heartbeat] started
2026-04-14T02:35:10.252+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T02:35:10.256+08:00 [gateway] agent model: zai/zai_pony-alpha-2
2026-04-14T02:35:10.258+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 20484)
2026-04-14T02:35:10.261+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
[GatewayManager] Optimization post-ready: warmupSpawned=true pid=177252 cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Startup phase: compile-cache warmup spawn took 105ms
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=7100 compileCache=true warmup=true
2026-04-14T02:35:10.313+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
2026-04-14T02:36:58.167+08:00 [ws] webchat connected conn=3e44bbd0-fbff-4f7f-b7f9-7e9a9b8b3678 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-14T02:36:59.406+08:00 [ws] ⇄ res ✓ config.get 1108ms conn=3e44bbd0…3678 id=7f638e45…2bc2
2026-04-14T02:36:59.721+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models, agents.defaults.compaction.mode)
2026-04-14T02:36:59.725+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T02:37:34.350+08:00 [ws] webchat disconnected code=1000 reason=client disconnect conn=3e44bbd0-fbff-4f7f-b7f9-7e9a9b8b3678
2026-04-14T02:37:34.890+08:00 [reload] config reload skipped (invalid config): plugins.slots.memory: plugin not found: memory-core
EXIT
[GatewayManager] Startup phase: prepare runtime took 1ms
[GatewayManager] Startup phase: sync settings catalog took 7ms
[GatewayManager] Startup phase: sanitize openclaw config took 13ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=3242, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 3246ms
[GatewayManager] Startup phase: ensure builtin skills took 23ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 0ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 506ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 239ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 517ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 1ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 132ms
[GatewayManager] Startup phase: patch gateway runtime took 1426ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T02:37:45.622+08:00 [gateway] force: no listeners on port 18789
2026-04-14T02:37:45.697+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T02:37:45.712+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 8c08ab08f87aae17cd5ced93f530ff37b269a60d05137cf26657a2cabcd0f379 -> 780748bc8caf94f1a90b4641635f884077df8839ad265249859258134c174981, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T02:37:45.715+08:00 Config write anomaly: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (missing-meta-before-write)
2026-04-14T02:37:45.721+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T02:37:45.736+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T02:38:03.361+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T02:38:10.378+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T02:38:10.382+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T02:38:10.390+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T02:38:10.392+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T02:38:10.395+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T02:38:10.400+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T02:38:10.402+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-14T02:38:12.734+08:00 [wecom] v1.0.13 loaded
2026-04-14T02:38:12.739+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T02:38:12.772+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T02:38:12.796+08:00 [heartbeat] started
2026-04-14T02:38:12.801+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T02:38:12.805+08:00 [gateway] agent model: zai/zai_pony-alpha-2
2026-04-14T02:38:12.807+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 139640)
2026-04-14T02:38:12.810+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
2026-04-14T02:38:12.858+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=30705 compileCache=true warmup=true
2026-04-14T02:38:13.252+08:00 [ws] webchat connected conn=2ee642cb-8d5d-410d-818f-1af635f63755 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-14T02:38:16.374+08:00 [ws] ⇄ res ✓ config.get 3103ms conn=2ee642cb…3755 id=5c29fbe3…316c
2026-04-14T02:38:53.466+08:00 [ws] ⇄ res ✓ skills.status 1448ms conn=2ee642cb…3755 id=88f5ff00…a6f6
2026-04-14T02:38:53.868+08:00 [ws] ⇄ res ✓ skills.status 379ms conn=2ee642cb…3755 id=748f554e…e56a
2026-04-14T02:38:54.182+08:00 [ws] ⇄ res ✓ skills.status 308ms conn=2ee642cb…3755 id=b500e797…6fdc
2026-04-14T02:38:54.193+08:00 [ws] ⇄ res ✓ config.get 323ms conn=2ee642cb…3755 id=caf25278…25b4
2026-04-14T02:40:14.605+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=zai_pony-alpha-2 body.model=pony-alpha-2 requestId=e7eeef6c-97f6-4ecb-804b-17621847f65a xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:40:26.179+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=zai_pony-alpha-2 requestId=e7eeef6c-97f6-4ecb-804b-17621847f65a xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:40:29.373+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=zai_pony-alpha-2 body.model=pony-alpha-2 requestId=9bda2183-051b-44f1-a0e2-36b9276da029 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:40:37.305+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=zai_pony-alpha-2 requestId=9bda2183-051b-44f1-a0e2-36b9276da029 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:47:04.901+08:00 [ws] webchat disconnected code=1000 reason=client disconnect conn=2ee642cb-8d5d-410d-818f-1af635f63755
2026-04-14T02:47:05.452+08:00 [reload] config change detected; evaluating reload (agents.defaults.model.primary)
2026-04-14T02:47:05.461+08:00 [reload] config hot reload applied (agents.defaults.model.primary)
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 4ms
[GatewayManager] Startup phase: sanitize openclaw config took 10ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=3329, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 3330ms
[GatewayManager] Startup phase: ensure builtin skills took 16ms
[GatewayManager] Startup phase: ensure skill path guidance took 0ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 1ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 491ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 243ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 539ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 1ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 123ms
[GatewayManager] Startup phase: patch gateway runtime took 1427ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T02:47:15.798+08:00 [gateway] force: no listeners on port 18789
2026-04-14T02:47:15.867+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T02:47:15.879+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 5b06e968f7c64a5ced7a12faa46b43240548afd25032978d04faef0655d35655 -> f40d5c5396c82e24d6df7ecc07fa3f8376df21564e3b61fa1ba3d16126e8ba02, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T02:47:15.884+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T02:47:15.896+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T02:47:21.732+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T02:47:22.567+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T02:47:22.570+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T02:47:22.577+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T02:47:22.579+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T02:47:22.583+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T02:47:22.586+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T02:47:22.588+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-14T02:47:24.305+08:00 [wecom] v1.0.13 loaded
2026-04-14T02:47:24.308+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T02:47:24.337+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T02:47:24.380+08:00 [heartbeat] started
2026-04-14T02:47:24.385+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T02:47:24.389+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-14T02:47:24.391+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 34496)
2026-04-14T02:47:24.394+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
2026-04-14T02:47:24.434+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=11834 compileCache=true warmup=true
2026-04-14T02:47:24.637+08:00 [ws] webchat connected conn=1e8df202-4ea0-4144-a9d8-248637c1a6d5 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-14T02:47:26.521+08:00 [ws] ⇄ res ✓ config.get 1863ms conn=1e8df202…a6d5 id=76f03e44…0724
2026-04-14T02:49:12.663+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=ec84c245-d296-4e2a-b47d-1936ac240244 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:49:17.433+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=ec84c245-d296-4e2a-b47d-1936ac240244 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:49:44.374+08:00 [tools] web_fetch failed: fetch failed
2026-04-14T02:49:44.388+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=de16b19f-d1a3-436f-82d6-3ddbca106639 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:49:49.562+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=de16b19f-d1a3-436f-82d6-3ddbca106639 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:01.728+08:00 [tools] web_fetch failed: fetch failed
2026-04-14T02:50:01.748+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=24f5f1e4-17eb-41f2-b862-d4212cf1046c xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:06.652+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=24f5f1e4-17eb-41f2-b862-d4212cf1046c xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:07.587+08:00 [security] blocked URL fetch (url-fetch) target=https://www.google.com/search reason=Blocked: resolves to private/internal/special-use IP address
2026-04-14T02:50:07.590+08:00 [tools] web_fetch failed: Blocked: resolves to private/internal/special-use IP address
2026-04-14T02:50:07.603+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=361748d8-6faa-4a18-bf0a-9cc7f94e1eac xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:13.905+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=361748d8-6faa-4a18-bf0a-9cc7f94e1eac xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:14.322+08:00 [tools] read failed: Path escapes sandbox root (~\.openclaw-autoclaw\workspace): C:\Users\Administrator\.openclaw-autoclaw\skills\autoglm-websearch\SKILL.md
2026-04-14T02:50:14.335+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=1a5825e1-8d21-430e-a7fa-22988a1c6a83 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:20.152+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=1a5825e1-8d21-430e-a7fa-22988a1c6a83 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:21.035+08:00 [tools] read failed: Path escapes sandbox root (~\.openclaw-autoclaw\workspace): ~/.openclaw-autoclaw/skills/autoglm-websearch/SKILL.md
2026-04-14T02:50:21.046+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=9416d8e2-1115-4dd6-bcf4-e55f56c8250e xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:25.707+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=9416d8e2-1115-4dd6-bcf4-e55f56c8250e xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:32.212+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=b6d2382c-6e57-43e2-aa5b-5539b9fb7c4a xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:39.905+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=b6d2382c-6e57-43e2-aa5b-5539b9fb7c4a xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:42.047+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=098b652e-d078-4d45-8399-17a957c8e416 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:49.280+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=098b652e-d078-4d45-8399-17a957c8e416 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:50:55.755+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=a405450b-dc4a-44a1-a818-4bdd5cba6da4 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:00.970+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=a405450b-dc4a-44a1-a818-4bdd5cba6da4 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:05.995+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=0a48b123-2679-4267-bc94-1b355bc61e46 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:10.785+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=0a48b123-2679-4267-bc94-1b355bc61e46 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:17.327+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=59b93fd3-6723-44dd-a572-76b7651f4c63 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:21.819+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=59b93fd3-6723-44dd-a572-76b7651f4c63 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:25.459+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=126eb5d2-3701-4efa-bc0d-18d87fd7b29a xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:30.107+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=126eb5d2-3701-4efa-bc0d-18d87fd7b29a xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:36.602+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=fc63fbc2-fa68-4e62-8454-07b637169a84 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:41.167+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=fc63fbc2-fa68-4e62-8454-07b637169a84 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:52.408+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=c3cb5909-5282-4a51-8200-d2ceb985563c xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:51:59.810+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=c3cb5909-5282-4a51-8200-d2ceb985563c xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:52:05.697+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=995fcf1c-dea2-4cd3-8df1-d860e9c0702b xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:52:10.739+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=995fcf1c-dea2-4cd3-8df1-d860e9c0702b xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:52:23.414+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=6ff529f3-e2d5-484d-8ecc-1850f178f7c0 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:52:29.877+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=6ff529f3-e2d5-484d-8ecc-1850f178f7c0 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:52:36.776+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=cd2289c1-9300-48d4-9122-467b80b87ffa xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:52:42.480+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=cd2289c1-9300-48d4-9122-467b80b87ffa xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:52:53.982+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=42beafde-4912-4785-ae4c-25bf05356d52 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:53:00.755+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=42beafde-4912-4785-ae4c-25bf05356d52 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:53:32.651+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=89330c22-a4b1-45bf-9ffc-12a8f3d2eee3 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:53:38.249+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=89330c22-a4b1-45bf-9ffc-12a8f3d2eee3 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:53:49.967+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=9a17c50f-ef85-443b-83e1-0d9c77602cf4 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:53:56.578+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=9a17c50f-ef85-443b-83e1-0d9c77602cf4 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:54:03.499+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=f9f1ce9f-a9b4-4c4e-bdc9-bf1ed1084e9d xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:54:09.151+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=f9f1ce9f-a9b4-4c4e-bdc9-bf1ed1084e9d xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:54:20.201+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=c57bf133-8c58-4988-94bf-d4147322b75a xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:54:20.579+08:00 [pi-ai] [AutoClawRequestTrace] fetch_error method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 requestId=c57bf133-8c58-4988-94bf-d4147322b75a xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main error=This operation was aborted
2026-04-14T02:54:24.232+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=2160ce4d-1c0f-48f7-8386-ab66a27a1654 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:54:31.206+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=2160ce4d-1c0f-48f7-8386-ab66a27a1654 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:54:39.471+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=1ee43bda-6c88-4fff-bdfb-a0472ab80c9e xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:54:44.608+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=1ee43bda-6c88-4fff-bdfb-a0472ab80c9e xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:54:58.783+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=1953003a-4e20-4b9c-88e8-7c41aeb07e62 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:55:03.204+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=1953003a-4e20-4b9c-88e8-7c41aeb07e62 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:55:05.775+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=1d5091ee-c6a4-470d-a2d4-b1eeba12a76b xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:55:12.430+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=1d5091ee-c6a4-470d-a2d4-b1eeba12a76b xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:55:35.455+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=be92cad2-8e42-4b14-9e07-d4b3de206784 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:55:42.238+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=be92cad2-8e42-4b14-9e07-d4b3de206784 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:55:43.525+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=d1bc2de7-d28f-4834-8ae1-308106ccec20 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:55:48.366+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=d1bc2de7-d28f-4834-8ae1-308106ccec20 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:56:00.356+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=39911f08-2289-4dbd-8756-8c5e42cca1d1 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:56:05.147+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=39911f08-2289-4dbd-8756-8c5e42cca1d1 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:56:21.551+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=bf879229-c342-41da-a7c6-02b14cc72151 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:56:27.434+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=bf879229-c342-41da-a7c6-02b14cc72151 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:56:53.217+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=8c3ce1a3-7faf-422e-8276-f84d96f67ae3 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:56:59.784+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=8c3ce1a3-7faf-422e-8276-f84d96f67ae3 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:56:59.812+08:00 [tools] read failed: Path escapes sandbox root (~\.openclaw-autoclaw\workspace): E:\OhMyOpenAgent\search.html
2026-04-14T02:56:59.829+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=0eefd20f-f926-42bd-b5ac-6406c248ef64 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:57:06.650+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=0eefd20f-f926-42bd-b5ac-6406c248ef64 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:57:10.980+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=99675490-0a81-4745-b1d8-6d7d9d756f49 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:57:16.785+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=99675490-0a81-4745-b1d8-6d7d9d756f49 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:57:19.032+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=5026e862-ef13-4099-bd20-a1aa62eecf54 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:57:26.790+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=5026e862-ef13-4099-bd20-a1aa62eecf54 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:57:41.620+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=74549f44-3ce1-4f42-b6a4-b53a54af0b27 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:57:46.367+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=74549f44-3ce1-4f42-b6a4-b53a54af0b27 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:57:46.903+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=5551d98f-9b51-407d-af9e-d0f2412732d4 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:57:53.550+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=5551d98f-9b51-407d-af9e-d0f2412732d4 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:57:55.491+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=3bde22f0-d4b4-4669-9624-7bc71560c82e xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:58:03.967+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=3bde22f0-d4b4-4669-9624-7bc71560c82e xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:58:17.139+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=c34c7e60-4897-452d-bdd8-f8af862c421c xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:58:24.202+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=c34c7e60-4897-452d-bdd8-f8af862c421c xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:58:24.236+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=085f8a26-f904-4855-8569-5ec5046eea93 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:58:29.569+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=085f8a26-f904-4855-8569-5ec5046eea93 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:58:33.588+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=fd092596-b35e-4c36-98cd-ae039bf32a11 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:58:35.807+08:00 [pi-ai] [AutoClawRequestTrace] fetch_error method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 requestId=fd092596-b35e-4c36-98cd-ae039bf32a11 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main error=This operation was aborted
2026-04-14T02:58:39.464+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=c36e6ba9-145d-46f2-adf1-96b4fbe0043b xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:58:45.686+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=c36e6ba9-145d-46f2-adf1-96b4fbe0043b xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:59:05.063+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=697bf205-0ce5-4f7f-8da4-ddb126c074c0 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:59:13.476+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=697bf205-0ce5-4f7f-8da4-ddb126c074c0 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:59:17.187+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=68f73dae-807e-4f99-851f-7ad178208ea3 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:59:22.886+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=68f73dae-807e-4f99-851f-7ad178208ea3 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:59:22.959+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=a2855294-f812-495f-9d0d-ba09a8fe8b2e xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:59:28.247+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=a2855294-f812-495f-9d0d-ba09a8fe8b2e xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:59:31.364+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=efa30667-6960-4010-9519-1324a5aa7c90 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:59:37.694+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=efa30667-6960-4010-9519-1324a5aa7c90 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:59:37.756+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=056b57c7-9563-4785-8250-607464e0fba5 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T02:59:44.724+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=056b57c7-9563-4785-8250-607464e0fba5 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:00:34.647+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=eda904d7-07eb-41bc-8c2c-0fe2db0d8864 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:00:41.737+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=eda904d7-07eb-41bc-8c2c-0fe2db0d8864 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:00:44.695+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=95238e44-2fb0-4c4c-8903-81671b738481 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:00:51.749+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=95238e44-2fb0-4c4c-8903-81671b738481 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:01:14.231+08:00 [tools] gateway failed: raw required
2026-04-14T03:01:14.246+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=c610a6cc-7d66-4487-b075-eb99b1fd3ebf xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:01:20.390+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=c610a6cc-7d66-4487-b075-eb99b1fd3ebf xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:01:32.667+08:00 [ws] ⇄ res ✗ config.patch 8ms errorCode=INVALID_REQUEST errorMessage=invalid config: models.providers.zhipu.api: Invalid option: expected one of "openai-completions"|"openai-responses"|"openai-codex-responses"|"anthropic-messages"|"google-generative-ai"|"github-copilot"|"bedrock-converse-stream"|"ollama" conn=c8f8327a…dacb id=667f50eb…974b
2026-04-14T03:01:32.670+08:00 [tools] gateway failed: invalid config: models.providers.zhipu.api: Invalid option: expected one of "openai-completions"|"openai-responses"|"openai-codex-responses"|"anthropic-messages"|"google-generative-ai"|"github-copilot"|"bedrock-converse-stream"|"ollama"
2026-04-14T03:01:32.683+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=9efe697c-85ad-41c3-b4cd-280f5bf570aa xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:01:38.835+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=9efe697c-85ad-41c3-b4cd-280f5bf570aa xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:01:47.593+08:00 [gateway] config.patch write actor=gateway-client device=3e92734f93c15c9ace3461abd1ce79c0e48e660b58e2e6157120bb466defab90 ip=unknown-ip conn=c7c9422b-10ad-4dda-808b-bc63d700b8f3 changedPaths=models.providers.zhipu,agents.defaults.model.primary restartReason=config.patch
2026-04-14T03:01:47.598+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T03:01:47.611+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 f40d5c5396c82e24d6df7ecc07fa3f8376df21564e3b61fa1ba3d16126e8ba02 -> 9eaa383e8f8122a55cfbd344a262266dc79738201af2035bb696e4fe6863541d, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T03:01:47.619+08:00 [gateway] request handler failed: ConfigRuntimeRefreshError: Config was written to C:\Users\Administrator\.openclaw-autoclaw\openclaw.json, but runtime snapshot refresh failed: Environment variable "ZHIPUAI_API_KEY" is missing or empty.
2026-04-14T03:01:47.621+08:00 [ws] ⇄ res ✗ config.patch 35ms errorCode=UNAVAILABLE errorMessage=ConfigRuntimeRefreshError: Config was written to C:\Users\Administrator\.openclaw-autoclaw\openclaw.json, but runtime snapshot refresh failed: Environment variable "ZHIPUAI_API_KEY" is missing or empty. conn=c7c9422b…b8f3 id=5157a563…89f9
2026-04-14T03:01:47.624+08:00 [tools] gateway failed: ConfigRuntimeRefreshError: Config was written to C:\Users\Administrator\.openclaw-autoclaw\openclaw.json, but runtime snapshot refresh failed: Environment variable "ZHIPUAI_API_KEY" is missing or empty.
2026-04-14T03:01:47.637+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=8a8684a9-59ef-4f0b-87f5-3c13d57e30c2 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:01:48.179+08:00 [reload] config change detected; evaluating reload (meta.lastTouchedAt, models.providers.zhipu, agents.defaults.model.primary)
2026-04-14T03:01:48.183+08:00 [secrets] [SECRETS_RELOADER_DEGRADED] SecretRefResolutionError: Environment variable "ZHIPUAI_API_KEY" is missing or empty.
2026-04-14T03:01:48.185+08:00 [reload] config reload failed: SecretRefResolutionError: Environment variable "ZHIPUAI_API_KEY" is missing or empty.
2026-04-14T03:01:54.628+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=8a8684a9-59ef-4f0b-87f5-3c13d57e30c2 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:04:39.511+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=ff4e7bfb-d0f3-48a9-88b1-f702178c3ebe xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:04:46.396+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=ff4e7bfb-d0f3-48a9-88b1-f702178c3ebe xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:05:01.907+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=94658dc4-6981-4102-81a0-b3c7547711d3 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:05:09.368+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=94658dc4-6981-4102-81a0-b3c7547711d3 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:05:09.662+08:00 [gateway-tool] gateway tool: restart requested (delayMs=default, reason=应用智谱AI API Key 配置)
2026-04-14T03:05:09.675+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=80e0fd6e-9206-4a0e-87e9-f71254199029 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:05:16.758+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=80e0fd6e-9206-4a0e-87e9-f71254199029 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:05:26.797+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=a508b241-ace5-4493-aef4-3e4f9ba0870f xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:05:35.831+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=a508b241-ace5-4493-aef4-3e4f9ba0870f xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:05:41.948+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=932dd3e6-2b38-4525-9fd5-412c32c35910 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:05:48.659+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=932dd3e6-2b38-4525-9fd5-412c32c35910 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:06:15.911+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=1dab6164-d274-47c1-913a-12f76c6fb361 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:06:24.281+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=1dab6164-d274-47c1-913a-12f76c6fb361 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:06:39.357+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=79b72cb2-a51e-404e-91e0-655571cc76b3 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:06:41.907+08:00 [gateway] signal SIGUSR1 received
2026-04-14T03:06:41.911+08:00 [gateway] received SIGUSR1; restarting
2026-04-14T03:06:41.913+08:00 [gateway] draining 2 active task(s) and 1 active embedded run(s) before restart (timeout 90000ms)
2026-04-14T03:06:46.263+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=79b72cb2-a51e-404e-91e0-655571cc76b3 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:06:50.207+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=465ad368-ed4c-4fdb-9a70-82bac84217ce xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:06:56.812+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=465ad368-ed4c-4fdb-9a70-82bac84217ce xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:07:03.440+08:00 [tools] exec failed: elevated is not available right now (runtime=direct).
Failing gates: allowFrom (tools.elevated.allowFrom.<provider> / agents.list[].tools.elevated.allowFrom.<provider>)
Context: provider=webchat session=agent:main:main
Fix-it keys:
- tools.elevated.enabled
- tools.elevated.allowFrom.<provider>
- agents.list[].tools.elevated.enabled
- agents.list[].tools.elevated.allowFrom.<provider>
2026-04-14T03:07:03.455+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=d6f5d8ce-388b-443b-83e5-2a09ca222ce4 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:07:12.823+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=d6f5d8ce-388b-443b-83e5-2a09ca222ce4 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:07:20.967+08:00 [gateway] config.patch write actor=gateway-client device=3e92734f93c15c9ace3461abd1ce79c0e48e660b58e2e6157120bb466defab90 ip=unknown-ip conn=de403b15-eaa3-4a9b-b19e-3343d52af00e changedPaths=models.providers.zhipu.apiKey restartReason=config.patch
2026-04-14T03:07:20.973+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T03:07:21.012+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 9eaa383e8f8122a55cfbd344a262266dc79738201af2035bb696e4fe6863541d -> ac3030e2de104243773eff05c804ad7a5402db4659b460a344539f1ee3e79a65, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak, changedPaths=1)
2026-04-14T03:07:21.022+08:00 [ws] ⇄ res ✓ config.patch 61ms conn=de403b15…f00e id=7cb2faee…0e5d
2026-04-14T03:07:21.040+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=f8a65b43-ecd0-4aee-ba8d-cb820e44505b xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:07:21.570+08:00 [reload] config change detected; evaluating reload (meta.lastTouchedAt, models.providers.zhipu.apiKey)
2026-04-14T03:07:21.573+08:00 [secrets] [SECRETS_RELOADER_RECOVERED] Secret resolution recovered; runtime remained on last-known-good during the outage.
2026-04-14T03:07:21.576+08:00 [reload] config hot reload applied (models.providers.zhipu.apiKey)
2026-04-14T03:07:29.980+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=f8a65b43-ecd0-4aee-ba8d-cb820e44505b xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:07:31.020+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=d67c5ef2-30c2-42fa-9213-91f8da54dca2 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:07:37.786+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=d67c5ef2-30c2-42fa-9213-91f8da54dca2 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:07:53.074+08:00 [gateway] all active work drained
2026-04-14T03:07:53.094+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T03:07:53.099+08:00 [feishu] stopping feishu[default]
2026-04-14T03:07:53.102+08:00 [feishu] stopped feishu[default]
2026-04-14T03:07:53.105+08:00 [gmail-watcher] gmail watcher stopped
2026-04-14T03:07:53.116+08:00 [ws] webchat disconnected code=1012 reason=service restart conn=1e8df202-4ea0-4144-a9d8-248637c1a6d5
2026-04-14T03:07:53.122+08:00 [gateway] signal SIGUSR1 received
2026-04-14T03:07:53.125+08:00 [gateway] received SIGUSR1 during shutdown; ignoring
2026-04-14T03:07:53.129+08:00 [gateway] restart mode: in-process restart (win32: detached respawn unsupported without Scheduled Task markers)
2026-04-14T03:07:53.166+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T03:07:53.178+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T03:07:53.196+08:00 [heartbeat] started
2026-04-14T03:07:53.200+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T03:07:53.204+08:00 [gateway] agent model: zhipu/glm-4-flash
2026-04-14T03:07:53.206+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 34496)
2026-04-14T03:07:53.209+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
2026-04-14T03:07:53.221+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
2026-04-14T03:07:54.177+08:00 [ws] webchat connected conn=f196721c-ba17-4358-bc78-6985c640c6c0 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-14T03:09:52.780+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=f5dc1729-7acf-4acb-8706-cf7c9f0c2308 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:52.957+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=f5dc1729-7acf-4acb-8706-cf7c9f0c2308 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:53.437+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=f5dc1729-7acf-4acb-8706-cf7c9f0c2308 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:53.575+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=f5dc1729-7acf-4acb-8706-cf7c9f0c2308 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:54.396+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=f5dc1729-7acf-4acb-8706-cf7c9f0c2308 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:54.526+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=f5dc1729-7acf-4acb-8706-cf7c9f0c2308 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:54.536+08:00 [agent/embedded] embedded run agent end: runId=agent_mnxkheu5_4zasmy isError=true model=glm-4-flash provider=zhipu error=⚠️ API rate limit reached. Please try again later.
2026-04-14T03:09:56.576+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=ed548f4c-946d-4894-87d8-008ea7005eda xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:56.680+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=ed548f4c-946d-4894-87d8-008ea7005eda xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:57.066+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=ed548f4c-946d-4894-87d8-008ea7005eda xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:57.247+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=ed548f4c-946d-4894-87d8-008ea7005eda xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:58.161+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=ed548f4c-946d-4894-87d8-008ea7005eda xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:58.296+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=ed548f4c-946d-4894-87d8-008ea7005eda xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:09:58.302+08:00 [agent/embedded] embedded run agent end: runId=agent_mnxkheu5_4zasmy isError=true model=glm-4-flash provider=zhipu error=⚠️ API rate limit reached. Please try again later.
2026-04-14T03:10:02.335+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=a7346184-dfc4-46c7-845e-31904778dfe9 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:02.518+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=a7346184-dfc4-46c7-845e-31904778dfe9 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:02.932+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=a7346184-dfc4-46c7-845e-31904778dfe9 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:03.060+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=a7346184-dfc4-46c7-845e-31904778dfe9 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:03.936+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=a7346184-dfc4-46c7-845e-31904778dfe9 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:04.106+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=a7346184-dfc4-46c7-845e-31904778dfe9 xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:04.112+08:00 [agent/embedded] embedded run agent end: runId=agent_mnxkheu5_4zasmy isError=true model=glm-4-flash provider=zhipu error=⚠️ API rate limit reached. Please try again later.
2026-04-14T03:10:12.146+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=1fa5b81d-4c10-479e-a32d-051629d4fbea xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:12.280+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=1fa5b81d-4c10-479e-a32d-051629d4fbea xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:12.696+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=1fa5b81d-4c10-479e-a32d-051629d4fbea xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:12.833+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=1fa5b81d-4c10-479e-a32d-051629d4fbea xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:13.746+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions provider=zhipu model.id=glm-4-flash body.model=glm-4-flash requestId=1fa5b81d-4c10-479e-a32d-051629d4fbea xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:13.864+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://open.bigmodel.cn/api/paas/v4/chat/completions status=429 provider=zhipu model.id=glm-4-flash requestId=1fa5b81d-4c10-479e-a32d-051629d4fbea xSessionId=c5dac8f1-c203-4b68-bd6d-535ab64e1c11 xAgentId=main
2026-04-14T03:10:13.870+08:00 [agent/embedded] embedded run agent end: runId=agent_mnxkheu5_4zasmy isError=true model=glm-4-flash provider=zhipu error=⚠️ API rate limit reached. Please try again later.
2026-04-14T03:10:13.885+08:00 [agent/embedded] embedded run failover decision: runId=agent_mnxkheu5_4zasmy stage=assistant decision=surface_error reason=rate_limit provider=zhipu/glm-4-flash profile=-
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 5ms
[GatewayManager] Startup phase: sanitize openclaw config took 13ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=2952, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 2955ms
[GatewayManager] Startup phase: ensure builtin skills took 17ms
[GatewayManager] Startup phase: ensure skill path guidance took 0ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 1ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 466ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 235ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 517ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 121ms
[GatewayManager] Startup phase: patch gateway runtime took 1394ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T11:48:53.855+08:00 [gateway] force: no listeners on port 18789
2026-04-14T11:48:53.922+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T11:48:53.937+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 d7766db8d5bd2bcad0ea585df822bb4dc39d05239e925e3433652bac26796e81 -> 118fc518eba3bcadc571746ddccd9cddcf43124df0f0c499512cc8410bd21956, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T11:48:53.942+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T11:48:53.952+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T11:48:59.548+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T11:49:00.351+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T11:49:00.354+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T11:49:00.361+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T11:49:00.364+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T11:49:00.366+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T11:49:00.371+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T11:49:00.372+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-14T11:49:02.086+08:00 [wecom] v1.0.13 loaded
2026-04-14T11:49:02.090+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T11:49:02.120+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T11:49:02.144+08:00 [heartbeat] started
2026-04-14T11:49:02.147+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T11:49:02.152+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-14T11:49:02.154+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 184964)
2026-04-14T11:49:02.157+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
2026-04-14T11:49:02.197+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
[GatewayManager] Optimization post-ready: warmupSpawned=true pid=187856 cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Startup phase: compile-cache warmup spawn took 124ms
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=17635 compileCache=true warmup=true
2026-04-14T11:49:08.767+08:00 [ws] webchat connected conn=a0d85fa0-c26b-4abf-a425-fea097e17297 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-14T11:49:10.077+08:00 [ws] ⇄ res ✓ config.get 1293ms conn=a0d85fa0…7297 id=594d46b9…b3d1
2026-04-14T12:48:46.765+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T12:48:46.777+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T13:12:37.299+08:00 [ws] ⇄ res ✓ sessions.list 102ms conn=a0d85fa0…7297 id=6483719c…399e
EXIT
[GatewayManager] Startup phase: prepare runtime took 1ms
[GatewayManager] Startup phase: sync settings catalog took 8ms
[GatewayManager] Startup phase: sanitize openclaw config took 25ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=5627, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 5631ms
[GatewayManager] Startup phase: ensure builtin skills took 124ms
[GatewayManager] Startup phase: ensure skill path guidance took 2ms
[GatewayManager] Startup phase: pre-register device took 2ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 1559ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 427ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 954ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 199ms
[GatewayManager] Startup phase: patch gateway runtime took 3169ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:17:41.361+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:17:41.455+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:17:41.480+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 955e5efd98fa5dc673c2a3768083f746f359f925bee391c1acef9047470b9d2c -> 314acbaf38e873c86c38e9f9833b3b657050cdc5ddbd472bda7f6b8bf3c8eddf, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:17:41.488+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:17:41.504+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=6909 compileCache=true warmup=true
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 7ms
[GatewayManager] Startup phase: sanitize openclaw config took 16ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=4378, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 4382ms
[GatewayManager] Startup phase: ensure builtin skills took 36ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 1ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 849ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 1ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 427ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 865ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 205ms
[GatewayManager] Startup phase: patch gateway runtime took 2401ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:17:59.723+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:17:59.793+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:17:59.810+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 7f48771f8929add1de789bb136dca1d67c1b7ff4bc671c60d3348e1e6e1c7d79 -> df38eb4b0a1ecafae79810be08995303d70549b050519584b4dbc0fc177c9a27, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:17:59.816+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:17:59.826+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=9823 compileCache=true warmup=true
2026-04-14T13:18:09.488+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 6ms
[GatewayManager] Startup phase: sanitize openclaw config took 16ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=3505, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 3509ms
[GatewayManager] Startup phase: ensure builtin skills took 32ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 2ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 1ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 956ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 399ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 929ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 188ms
[GatewayManager] Startup phase: patch gateway runtime took 2501ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:18:22.119+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:18:22.199+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:18:22.214+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 fcb725b6c96b81281f9d9b3c400602de7c3c9fceda91b4aa439dad74403d372e -> 1051ead7cebab1ea737b2f1829578a6daaf09028416a24d290b1b2adc6af7012, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:18:22.219+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:18:22.229+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=7267 compileCache=true warmup=true
2026-04-14T13:18:28.448+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:18:30.075+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T13:18:30.079+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T13:18:30.091+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T13:18:30.095+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T13:18:30.098+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T13:18:30.103+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T13:18:30.107+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-14T13:18:33.185+08:00 [wecom] v1.0.13 loaded
2026-04-14T13:18:33.192+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T13:18:33.235+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T13:18:35.250+08:00 Gateway failed to start: another gateway instance is already listening on ws://127.0.0.1:18789
If the gateway is supervised, stop it with: openclaw gateway stop
2026-04-14T13:18:35.905+08:00 Port 18789 is already in use.
2026-04-14T13:18:35.909+08:00 - pid 212840: "C:\Users\Administrator\AppData\Local\Programs\ClawX\ClawX.exe" --type=utility --utility-sub-type=node.mojom.NodeService --lang=zh-CN --service-sandbox-type=none --user-data-dir="C:\Users\Administrator\AppData\Roaming\clawx" --field-trial-handle=1888,i,12855811106993971359,16297551446451880645,262144 --enable-features=EnableTransparentHwndEnlargement,PdfUseShowSaveFilePicker --disable-features=LocalNetworkAccessChecks,NetworkServiceSandbox,ScreenAIOCREnabled,SpareRendererForSitePerProcess,TraceSiteInstanceGetProcessCreation --variations-seed-version --trace-process-track-uuid=3190708992871164437 --mojo-platform-channel-handle=4060 /prefetch:8 (127.0.0.1:18789)
2026-04-14T13:18:35.913+08:00 - Another process is listening on this port.
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 6ms
[GatewayManager] Startup phase: sanitize openclaw config took 14ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=3004, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 3007ms
[GatewayManager] Startup phase: ensure builtin skills took 33ms
[GatewayManager] Startup phase: ensure skill path guidance took 0ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 3ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 1ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 843ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 404ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 830ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 193ms
[GatewayManager] Startup phase: patch gateway runtime took 2311ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:20:46.224+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:20:46.263+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:20:46.308+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 a4ef35c6098befa4db4e616c1dafef54a11f5bce2f7eebbd0c2486d08aeed47b -> a8f3783d2ae9c533adaf4fd5348eb271a93e41baf7d12363d6e293ce521b544a, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:20:46.313+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:20:46.324+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:20:52.086+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:20:53.716+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T13:20:53.721+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T13:20:53.736+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T13:20:53.740+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T13:20:53.744+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T13:20:53.752+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T13:20:53.755+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-14T13:20:57.019+08:00 [wecom] v1.0.13 loaded
2026-04-14T13:20:57.026+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T13:20:57.072+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T13:20:57.110+08:00 [heartbeat] started
2026-04-14T13:20:57.116+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T13:20:57.122+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-14T13:20:57.126+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 212052)
2026-04-14T13:20:57.131+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
2026-04-14T13:20:57.197+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=13922 compileCache=true warmup=true
2026-04-14T13:20:57.236+08:00 [ws] closed before connect conn=91105560-b7e3-4e99-a02b-8d16db1a8bbe remote=::1 fwd=n/a origin=n/a host=localhost:18789 ua=n/a code=1005 reason=n/a
2026-04-14T13:20:57.257+08:00 [ws] unauthorized conn=a6d857dd-d78c-42db-9736-72bf9fb9c305 remote=::1 client=ClawX ui v0.1.0 reason=token_mismatch
2026-04-14T13:20:57.265+08:00 [ws] closed before connect conn=a6d857dd-d78c-42db-9736-72bf9fb9c305 remote=::1 fwd=n/a origin=n/a host=localhost:18789 ua=n/a code=1008 reason=unauthorized: gateway token mismatch (provide gateway auth token)
2026-04-14T13:20:57.820+08:00 [ws] webchat connected conn=a156c35f-e50a-4046-8d11-a6d7f3f28432 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 7ms
[GatewayManager] Startup phase: sanitize openclaw config took 15ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=3533, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 3537ms
[GatewayManager] Startup phase: ensure builtin skills took 35ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 3ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 1ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 943ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 452ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 902ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 210ms
[GatewayManager] Startup phase: patch gateway runtime took 2537ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:21:19.056+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:21:19.155+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:21:19.175+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 90c7227dcf2173cca9fc6c0a2a4266497525ec0090d4a2bcd2d40ed9287cc60a -> c38238e426f80b88827f025a36a5a9e1e16494edfe16a7c14b6a78b567f28f2c, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:21:19.181+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:21:19.196+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=8847 compileCache=true warmup=true
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 7ms
[GatewayManager] Startup phase: sanitize openclaw config took 16ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=3957, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 3961ms
[GatewayManager] Startup phase: ensure builtin skills took 37ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 3ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 914ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 1ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 440ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 888ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 203ms
[GatewayManager] Startup phase: patch gateway runtime took 2477ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:21:40.946+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:21:41.023+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:21:41.040+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 57fd12225bdcb697c4bab43a4cdc38883feb356de2822dffe874bedf4926881f -> 34851a93bde35627a65346c0c9f4fe3b1d5420811584afb8faee3bbe06c7a85b, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:21:41.046+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:21:41.056+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=7879 compileCache=true warmup=true
2026-04-14T13:21:49.672+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:21:51.459+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T13:21:51.464+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T13:21:51.476+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T13:21:51.480+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T13:21:51.484+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T13:21:51.489+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T13:21:51.492+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-14T13:21:54.793+08:00 [wecom] v1.0.13 loaded
2026-04-14T13:21:54.799+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T13:21:54.847+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T13:21:54.887+08:00 [heartbeat] started
2026-04-14T13:21:54.894+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T13:21:54.901+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-14T13:21:54.904+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 208168)
2026-04-14T13:21:54.909+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
2026-04-14T13:21:54.974+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
2026-04-14T13:21:55.005+08:00 [ws] closed before connect conn=d60d2a87-fe15-4a15-9288-65d4401ae198 remote=::1 fwd=n/a origin=n/a host=localhost:18789 ua=n/a code=1005 reason=n/a
2026-04-14T13:21:55.025+08:00 [ws] unauthorized conn=92fb14f4-c47c-41ee-b543-cad412d14128 remote=::1 client=ClawX ui v0.1.0 reason=token_mismatch
2026-04-14T13:21:55.031+08:00 [ws] closed before connect conn=92fb14f4-c47c-41ee-b543-cad412d14128 remote=::1 fwd=n/a origin=n/a host=localhost:18789 ua=n/a code=1008 reason=unauthorized: gateway token mismatch (provide gateway auth token)
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 6ms
[GatewayManager] Startup phase: sanitize openclaw config took 18ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=5133, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 5137ms
[GatewayManager] Startup phase: ensure builtin skills took 93ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 2ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 2ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 1ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 1471ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 428ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 893ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 203ms
[GatewayManager] Startup phase: patch gateway runtime took 3024ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:24:49.955+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:24:50.034+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:24:50.049+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 12a8bd785ea3b25d83d9381aae90356d80dae29d83d6afea9202e8bdcda5a247 -> 007bc1114f2c0928f41bf9d0b6756a72337dcfb36ecd42cc27fba0f59c2a7467, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:24:50.054+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:24:50.065+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:25:00.028+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:25:02.215+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T13:25:02.220+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T13:25:02.234+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T13:25:02.238+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T13:25:02.242+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T13:25:02.247+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T13:25:02.251+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=16450 compileCache=true warmup=true
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 7ms
[GatewayManager] Startup phase: sanitize openclaw config took 19ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=3371, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 3375ms
[GatewayManager] Startup phase: ensure builtin skills took 83ms
[GatewayManager] Startup phase: ensure skill path guidance took 2ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 2ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 905ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 404ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 844ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 2ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 203ms
[GatewayManager] Startup phase: patch gateway runtime took 2389ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:25:18.470+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:25:18.551+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:25:18.570+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 477c89ee0de3446c53a5c664449b36179e19429db0a59609b75d355597d257c2 -> d8086a66068461f28384eb9b205f9c8ec2024a08bb037f6794506ab58ecc9b41, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:25:18.575+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:25:18.586+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:25:26.890+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:25:28.823+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T13:25:28.827+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T13:25:28.841+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T13:25:28.845+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T13:25:28.848+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T13:25:28.853+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T13:25:28.857+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-14T13:25:32.194+08:00 [wecom] v1.0.13 loaded
2026-04-14T13:25:32.201+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T13:25:32.262+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T13:25:32.301+08:00 [heartbeat] started
2026-04-14T13:25:32.308+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T13:25:32.316+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-14T13:25:32.319+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 210416)
2026-04-14T13:25:32.325+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
2026-04-14T13:25:32.390+08:00 [ws] closed before connect conn=78942c85-d8ea-46f5-b25b-f115b356137e remote=::1 fwd=n/a origin=n/a host=localhost:18789 ua=n/a code=1005 reason=n/a
2026-04-14T13:25:32.416+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
2026-04-14T13:25:32.454+08:00 [ws] unauthorized conn=ed6310d8-4e8d-4dea-8235-a4942fcf5692 remote=::1 client=ClawX ui v0.1.0 reason=token_mismatch
2026-04-14T13:25:32.462+08:00 [ws] closed before connect conn=ed6310d8-4e8d-4dea-8235-a4942fcf5692 remote=::1 fwd=n/a origin=n/a host=localhost:18789 ua=n/a code=1008 reason=unauthorized: gateway token mismatch (provide gateway auth token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=17444 compileCache=true warmup=true
2026-04-14T13:25:33.583+08:00 [ws] webchat connected conn=20f3cbcd-2305-4784-ac53-1cb30b9cec32 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 7ms
[GatewayManager] Startup phase: sanitize openclaw config took 24ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=5241, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 5246ms
[GatewayManager] Startup phase: ensure builtin skills took 81ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 1207ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 411ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 897ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 2ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 191ms
[GatewayManager] Startup phase: patch gateway runtime took 2749ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:26:14.375+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:26:14.452+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:26:14.469+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 11188d9741737577573c2eafb4c5af1852091481e6a1cc7a8837964da4fe97e0 -> 895bd7a2e32fe76999c86afb0344124e30f74dda31cba6e75d58dc7e3d751d40, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:26:14.475+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:26:14.485+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:26:22.488+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:26:23.668+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T13:26:23.671+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T13:26:23.680+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T13:26:23.682+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T13:26:23.684+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T13:26:23.687+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T13:26:23.689+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-14T13:26:25.512+08:00 [wecom] v1.0.13 loaded
2026-04-14T13:26:25.517+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T13:26:25.544+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T13:26:25.569+08:00 [heartbeat] started
2026-04-14T13:26:25.572+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T13:26:25.577+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-14T13:26:25.579+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 201968)
2026-04-14T13:26:25.582+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
2026-04-14T13:26:25.628+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=14441 compileCache=true warmup=true
2026-04-14T13:26:25.712+08:00 [ws] closed before connect conn=e3132ade-1be0-4d7d-8006-f7eed131aba2 remote=::1 fwd=n/a origin=n/a host=localhost:18789 ua=n/a code=1005 reason=n/a
2026-04-14T13:26:25.724+08:00 [ws] unauthorized conn=6026fa53-2f55-4b98-a838-634dc4600534 remote=::1 client=ClawX ui v0.1.0 reason=token_mismatch
2026-04-14T13:26:25.733+08:00 [ws] closed before connect conn=6026fa53-2f55-4b98-a838-634dc4600534 remote=::1 fwd=n/a origin=n/a host=localhost:18789 ua=n/a code=1008 reason=unauthorized: gateway token mismatch (provide gateway auth token)
2026-04-14T13:26:26.475+08:00 [ws] webchat connected conn=9796ff06-7552-4d86-b1cd-455254bf61ab remote=127.0.0.1 client=AutoClaw webchat v0.1.13
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 6ms
[GatewayManager] Startup phase: sanitize openclaw config took 19ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=4816, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 4819ms
[GatewayManager] Startup phase: ensure builtin skills took 81ms
[GatewayManager] Startup phase: ensure skill path guidance took 2ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 1ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 1307ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 481ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 971ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 4ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 219ms
[GatewayManager] Startup phase: patch gateway runtime took 3011ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:27:21.074+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:27:21.152+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:27:21.170+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 08c55bf1729ee05c24c58fa7025099850b8019325357b7962b8e013811231a84 -> 44d3ff28f3c71af8bcfab738efacfb1ec7ab0cf3d902db6f67924255c55525c5, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:27:21.176+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:27:21.187+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:27:30.073+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:27:31.792+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T13:27:31.796+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T13:27:31.809+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T13:27:31.813+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T13:27:31.816+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T13:27:31.822+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T13:27:31.826+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-14T13:27:34.992+08:00 [wecom] v1.0.13 loaded
2026-04-14T13:27:34.998+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T13:27:35.043+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T13:27:35.079+08:00 [heartbeat] started
2026-04-14T13:27:35.084+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T13:27:35.091+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-14T13:27:35.095+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 215076)
2026-04-14T13:27:35.099+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
2026-04-14T13:27:35.165+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
2026-04-14T13:27:35.191+08:00 [ws] closed before connect conn=574d6cca-7a57-409a-8345-1ffb2fe15f3a remote=::1 fwd=n/a origin=n/a host=localhost:18789 ua=n/a code=1005 reason=n/a
2026-04-14T13:27:35.212+08:00 [ws] unauthorized conn=7b5a68c3-2c54-4e71-b79b-01d7421c5f19 remote=::1 client=ClawX ui v0.1.0 reason=token_mismatch
2026-04-14T13:27:35.218+08:00 [ws] closed before connect conn=7b5a68c3-2c54-4e71-b79b-01d7421c5f19 remote=::1 fwd=n/a origin=n/a host=localhost:18789 ua=n/a code=1008 reason=unauthorized: gateway token mismatch (provide gateway auth token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=17954 compileCache=true warmup=true
2026-04-14T13:27:36.152+08:00 [ws] webchat connected conn=7c96258f-72da-475b-8456-fc660382797f remote=127.0.0.1 client=AutoClaw webchat v0.1.13
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 7ms
[GatewayManager] Startup phase: sanitize openclaw config took 19ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=5051, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 5055ms
[GatewayManager] Startup phase: ensure builtin skills took 84ms
[GatewayManager] Startup phase: ensure skill path guidance took 3ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 2ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 1296ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 1ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 436ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 905ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 2ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 205ms
[GatewayManager] Startup phase: patch gateway runtime took 2874ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:27:58.647+08:00 [gateway] force: no listeners on port 18789
2026-04-14T13:27:58.735+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:27:58.753+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 40fab6afeaf2f35290e814ca8dbf43ca71ddb656477990833abc4baaffeb049f -> 175ad91b55cf4753febcc88a788a40584c430e61b7e557314609fcebf355fd10, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:27:58.760+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:27:58.772+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=5818 compileCache=true warmup=true
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 6ms
[GatewayManager] Startup phase: sanitize openclaw config took 19ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=4559, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 4563ms
[GatewayManager] Startup phase: ensure builtin skills took 69ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 1388ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 439ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 892ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 191ms
[GatewayManager] Startup phase: patch gateway runtime took 2938ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-14T13:28:34.966+08:00 [gateway] force: no listeners on port 18790
2026-04-14T13:28:35.045+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:28:35.062+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 f0e6626b3d05e0ced4cb8d58d38f2d47c70c19b6cff0a1fdf57daeb6612c2ec5 -> de1560e38ce9ac1d0b8cdc15ad529a782d2492088fd4aea758aa651787ed9105, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-14T13:28:35.067+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-14T13:28:35.079+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:28:42.588+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-14T13:28:44.370+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-14T13:28:44.375+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-14T13:28:44.387+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-14T13:28:44.391+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-14T13:28:44.394+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-14T13:28:44.399+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-14T13:28:44.402+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-14T13:28:47.510+08:00 [wecom] v1.0.13 loaded
2026-04-14T13:28:47.516+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-14T13:28:47.561+08:00 [canvas] host mounted at http://127.0.0.1:18790/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-14T13:28:47.597+08:00 [heartbeat] started
2026-04-14T13:28:47.603+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-14T13:28:47.609+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-14T13:28:47.613+08:00 [gateway] listening on ws://127.0.0.1:18790, ws://[::1]:18790 (PID 216472)
2026-04-14T13:28:47.618+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-14.log
2026-04-14T13:28:47.680+08:00 [browser/server] Browser control listening on http://127.0.0.1:18792/ (auth=token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=15910 compileCache=true warmup=true
2026-04-14T13:28:48.650+08:00 [ws] webchat connected conn=223bc2f5-a39a-4d2a-b158-720c41bc07c5 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-14T13:28:52.082+08:00 [ws] ⇄ res ✓ config.get 3392ms conn=223bc2f5…07c5 id=9b923ee7…97d4
2026-04-14T13:36:57.428+08:00 [pi-ai] [AutoClawRequestTrace] request method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions provider=zai model.id=huawei_glm-5 body.model=glm-5 requestId=7b0d1177-f088-49a0-891b-0754b4e37b35 xSessionId=bc4443aa-963b-4da6-921a-f7dc3e10c954 xAgentId=main
2026-04-14T13:37:04.883+08:00 [pi-ai] [AutoClawRequestTrace] response method=POST url=https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions status=200 provider=zai model.id=huawei_glm-5 requestId=7b0d1177-f088-49a0-891b-0754b4e37b35 xSessionId=bc4443aa-963b-4da6-921a-f7dc3e10c954 xAgentId=main
2026-04-14T13:48:46.781+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T13:48:46.788+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T14:48:46.869+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T14:48:46.888+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T15:48:46.740+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T15:48:46.744+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T16:48:46.725+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T16:48:46.733+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T17:48:46.704+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T17:48:46.707+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T18:48:46.715+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T18:48:46.741+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T19:48:46.775+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T19:48:46.779+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T20:48:46.785+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T20:48:46.789+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T21:48:46.785+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T21:48:46.789+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T22:48:46.775+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T22:48:46.778+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-14T23:48:46.790+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-14T23:48:46.797+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T00:48:49.504+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T00:48:49.507+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T01:48:49.513+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T01:48:49.517+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T02:48:49.534+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T02:48:49.538+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T03:48:49.536+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T03:48:49.539+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T04:48:49.529+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T04:48:49.533+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T05:48:49.537+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T05:48:49.540+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T06:48:49.555+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T06:48:49.559+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T07:48:49.523+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T07:48:49.527+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T08:48:49.553+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T08:48:49.557+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T09:48:49.582+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T09:48:49.586+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T10:48:50.928+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T10:48:50.931+08:00 [reload] config hot reload applied (models.providers.zai.models)
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 13ms
[GatewayManager] Startup phase: sanitize openclaw config took 478ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=1, elapsedMs=26471, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 26494ms
[GatewayManager] Startup phase: ensure builtin skills took 315ms
[GatewayManager] Startup phase: ensure skill path guidance took 2ms
[GatewayManager] Startup phase: pre-register device took 5ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 5ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 7240ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 371ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 847ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 159ms
[GatewayManager] Startup phase: patch gateway runtime took 8783ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-15T11:38:38.763+08:00 [gateway] force: no listeners on port 18789
2026-04-15T11:38:38.813+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-15T11:38:38.874+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 18d86da035f85fb5a921af51dba4c0efb5dee1b0a3195c876682e602c12888b2 -> dc16061090a7c61b27c7fad6b87632591b5770eb60bc2d88639ec3bb8e30a6f1, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-15T11:38:38.881+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-15T11:38:38.896+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-15T11:38:49.735+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-15T11:38:51.447+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-15T11:38:51.453+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-15T11:38:51.464+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-15T11:38:51.467+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-15T11:38:51.470+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-15T11:38:51.474+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-15T11:38:51.477+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-15T11:38:54.256+08:00 [wecom] v1.0.13 loaded
2026-04-15T11:38:54.263+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-15T11:38:54.304+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-15T11:38:54.344+08:00 [heartbeat] started
2026-04-15T11:38:54.349+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-15T11:38:54.355+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-15T11:38:54.358+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 2588)
2026-04-15T11:38:54.362+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-15.log
2026-04-15T11:38:54.416+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
[GatewayManager] Optimization post-ready: warmupSpawned=true pid=3128 cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Startup phase: compile-cache warmup spawn took 65ms
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=27681 compileCache=true warmup=true
2026-04-15T11:38:54.750+08:00 [ws] webchat connected conn=7abbc434-7dc5-46e1-b2c1-ec0830a928a7 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-15T11:38:57.279+08:00 [ws] ⇄ res ✓ config.get 2509ms conn=7abbc434…28a7 id=bb4442f2…43e0
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 12ms
[GatewayManager] Startup phase: sanitize openclaw config took 100ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=1, elapsedMs=18270, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 18308ms
[GatewayManager] Startup phase: ensure builtin skills took 232ms
[GatewayManager] Startup phase: ensure skill path guidance took 2ms
[GatewayManager] Startup phase: pre-register device took 4ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 4ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 1ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 43835ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 1ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 431ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 831ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 1ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 165ms
[GatewayManager] Startup phase: patch gateway runtime took 45682ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-15T22:41:52.059+08:00 [gateway] force: no listeners on port 18789
2026-04-15T22:41:52.292+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-15T22:41:53.286+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 6bd8e8b18044f96dbe76e56246605aeb880e83497a77b84b16c3959ff5db9837 -> ff44d704d26616003cb80c1c664fe85ac2fe3b06461e3ccb67dece5b65c09fb7, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-15T22:41:53.742+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-15T22:41:53.781+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 298ms
[GatewayManager] Startup phase: sanitize openclaw config took 159ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=6335, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 6337ms
[GatewayManager] Startup phase: ensure builtin skills took 21ms
[GatewayManager] Startup phase: ensure skill path guidance took 0ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 892ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 345ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 571ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 3ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 3ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 133ms
[GatewayManager] Startup phase: patch gateway runtime took 2184ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-15T22:43:03.422+08:00 [gateway] force: no listeners on port 18789
2026-04-15T22:43:03.529+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-15T22:43:03.550+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 bfbdc2d585796cd56a4183c77377916e0a0256b0a0070a111d5a7974d3ac9564 -> 27883bc29aaef9b87c0bb1b72e5f46d7ef92dc427cffcabc850b30c35968d702, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-15T22:43:03.558+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-15T22:43:03.574+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-15T22:43:14.084+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-15T22:43:15.906+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-15T22:43:15.910+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-15T22:43:15.921+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-15T22:43:15.924+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-15T22:43:15.927+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-15T22:43:15.931+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-15T22:43:15.934+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-15T22:43:19.283+08:00 [wecom] v1.0.13 loaded
2026-04-15T22:43:19.289+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-15T22:43:19.337+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-15T22:43:19.396+08:00 [heartbeat] started
2026-04-15T22:43:19.402+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-15T22:43:19.409+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-15T22:43:19.413+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 14980)
2026-04-15T22:43:19.418+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-15.log
2026-04-15T22:43:19.486+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
[GatewayManager] Optimization post-ready: warmupSpawned=true pid=14356 cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Startup phase: compile-cache warmup spawn took 87ms
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=21147 compileCache=true warmup=true
2026-04-15T22:43:19.646+08:00 [ws] webchat connected conn=997f18cf-af40-4ef1-a7c1-e854835bd418 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-15T22:43:23.189+08:00 [ws] ⇄ res ✓ config.get 3515ms conn=997f18cf…d418 id=aaa13f41…25d7
2026-04-15T22:59:32.051+08:00 [ws] ⇄ res ✓ sessions.list 265ms conn=997f18cf…d418 id=5b79ecee…bac2
2026-04-15T23:08:29.521+08:00 [ws] ⇄ res ✓ sessions.list 61ms conn=997f18cf…d418 id=4f0268cc…8165
2026-04-15T23:40:35.314+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-15T23:40:35.373+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-15T23:58:31.708+08:00 [ws] ⇄ res ✓ sessions.list 417ms conn=997f18cf…d418 id=1e14ebf5…c241
2026-04-16T00:00:27.988+08:00 [ws] ⇄ res ✓ sessions.list 62ms conn=997f18cf…d418 id=fc85da11…1b51
2026-04-16T00:02:28.134+08:00 [ws] ⇄ res ✓ sessions.list 179ms conn=997f18cf…d418 id=c162d6f6…19dc
2026-04-16T00:40:34.831+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T00:40:34.879+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T01:04:28.146+08:00 [ws] ⇄ res ✓ sessions.list 122ms conn=997f18cf…d418 id=d7138855…34bd
2026-04-16T01:07:27.877+08:00 [ws] ⇄ res ✓ sessions.list 68ms conn=997f18cf…d418 id=90bf42ef…fe9c
2026-04-16T01:28:28.645+08:00 [ws] ⇄ res ✓ sessions.list 163ms conn=997f18cf…d418 id=f869289b…aff2
2026-04-16T01:33:28.010+08:00 [ws] ⇄ res ✓ sessions.list 53ms conn=997f18cf…d418 id=f024a0c7…d493
2026-04-16T01:40:34.204+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T01:40:34.213+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T02:40:34.250+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T02:40:34.261+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T03:40:34.226+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T03:40:34.238+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T04:40:34.139+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T04:40:34.147+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T05:40:34.151+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T05:40:34.157+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T06:40:34.158+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T06:40:34.166+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T07:40:34.188+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T07:40:34.194+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T11:40:34.257+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T11:40:34.271+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T12:40:34.280+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T12:40:34.285+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T13:40:34.252+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T13:40:34.257+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T14:40:34.245+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T14:40:34.252+08:00 [reload] config hot reload applied (models.providers.zai.models)
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 3ms
[GatewayManager] Startup phase: sanitize openclaw config took 35ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=6820, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 6824ms
[GatewayManager] Startup phase: ensure builtin skills took 118ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 3ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 1ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 1227ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 354ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 724ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 1ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 134ms
[GatewayManager] Startup phase: patch gateway runtime took 2488ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
2026-04-16T17:48:35.050+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-16T17:48:35.980+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 d12d0043fcd7f20e57f1331f21b14c58e1d5879893456a48cbb70675fc866af8 -> 4aa51436103c4daa39d527f96288903110d34326206e05c88ec129356def6578, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-16T17:48:36.211+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-16T17:48:34.843+08:00 [gateway] force: no listeners on port 18789
2026-04-16T17:48:36.178+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=-1 compileCache=true warmup=false
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 50ms
[GatewayManager] Startup phase: sanitize openclaw config took 14ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=1, elapsedMs=10122, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 10127ms
[GatewayManager] Startup phase: ensure builtin skills took 30ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 2ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 880ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 404ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 958ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 3ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 209ms
[GatewayManager] Startup phase: patch gateway runtime took 2533ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-16T17:50:22.138+08:00 [gateway] force: no listeners on port 18789
2026-04-16T17:50:22.230+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-16T17:50:22.293+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 a467a00c3cf76103a302e42623250429828254b6a01ea67094a23c434b0b26ce -> b5cf02097f2bfedad6036570a749b32b171cb1e34bfba15a942f9d2c6cc45ffe, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-16T17:50:22.300+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-16T17:50:22.319+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-16T17:50:48.744+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-16T17:51:02.646+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-16T17:51:02.652+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-16T17:51:02.665+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-16T17:51:02.669+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-16T17:51:02.673+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-16T17:51:02.678+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-16T17:51:02.681+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-16T17:51:17.920+08:00 [wecom] v1.0.13 loaded
2026-04-16T17:51:17.927+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-16T17:51:18.016+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-16T17:51:19.191+08:00 [heartbeat] started
2026-04-16T17:51:19.198+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-16T17:51:19.205+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-16T17:51:19.219+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 8892)
2026-04-16T17:51:19.224+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-16.log
[GatewayManager] Optimization post-ready: warmupSpawned=true pid=6824 cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Startup phase: compile-cache warmup spawn took 131ms
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=63613 compileCache=true warmup=true
2026-04-16T17:51:19.303+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
2026-04-16T17:51:19.568+08:00 [ws] webchat connected conn=a8d3597f-d7f0-4ea6-8da0-03abf1af396f remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-16T17:51:22.813+08:00 [ws] ⇄ res ✓ config.get 3212ms conn=a8d3597f…396f id=f7209863…4504
2026-04-16T17:55:13.326+08:00 [ws] ⇄ res ✓ sessions.list 6981ms conn=a8d3597f…396f id=541374c7…e661
2026-04-16T17:59:06.376+08:00 [ws] ⇄ res ✓ sessions.list 57ms conn=a8d3597f…396f id=d8bb81b7…f887
2026-04-16T18:01:06.395+08:00 [ws] ⇄ res ✓ sessions.list 84ms conn=a8d3597f…396f id=9e39a41d…9229
2026-04-16T18:02:06.402+08:00 [ws] ⇄ res ✓ sessions.list 90ms conn=a8d3597f…396f id=40fa0cbe…4f29
2026-04-16T18:03:06.365+08:00 [ws] ⇄ res ✓ sessions.list 53ms conn=a8d3597f…396f id=55991452…8254
2026-04-16T18:04:06.418+08:00 [ws] ⇄ res ✓ sessions.list 101ms conn=a8d3597f…396f id=d58cfc07…5233
2026-04-16T18:05:06.394+08:00 [ws] ⇄ res ✓ sessions.list 81ms conn=a8d3597f…396f id=1e453d69…2d09
2026-04-16T18:07:06.790+08:00 [ws] ⇄ res ✓ sessions.list 76ms conn=a8d3597f…396f id=18bfffc4…a2fe
2026-04-16T18:08:06.374+08:00 [ws] ⇄ res ✓ sessions.list 57ms conn=a8d3597f…396f id=ffd72af5…673c
2026-04-16T18:09:06.618+08:00 [ws] ⇄ res ✓ sessions.list 304ms conn=a8d3597f…396f id=6cff7fda…14c4
2026-04-16T18:10:06.482+08:00 [ws] ⇄ res ✓ sessions.list 68ms conn=a8d3597f…396f id=f6c066e7…b338
2026-04-16T18:11:06.632+08:00 [ws] ⇄ res ✓ sessions.list 314ms conn=a8d3597f…396f id=f86c318c…4412
2026-04-16T18:12:06.547+08:00 [ws] ⇄ res ✓ sessions.list 189ms conn=a8d3597f…396f id=92e9ed73…dbed
2026-04-16T18:13:06.394+08:00 [ws] ⇄ res ✓ sessions.list 84ms conn=a8d3597f…396f id=2ecec540…d6cc
EXIT
[GatewayManager] Startup phase: prepare runtime took 1ms
[GatewayManager] Startup phase: sync settings catalog took 4ms
[GatewayManager] Startup phase: sanitize openclaw config took 35ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=7866, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 7868ms
[GatewayManager] Startup phase: ensure builtin skills took 100ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 2ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 1ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 1083ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 366ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 726ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 4ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 147ms
[GatewayManager] Startup phase: patch gateway runtime took 2349ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-16T19:28:30.260+08:00 [gateway] force: no listeners on port 18789
2026-04-16T19:28:30.370+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-16T19:28:30.729+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 4c8564aaa272e0a1ed78b6f196c99d31e11e3ef5baafba669530d8a697cf1ff7 -> 8370bfb4b969d1fe8faf3969bfbc9aaff12d20f85621d4003ee2f2ee6560c544, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-16T19:28:30.774+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-16T19:28:30.816+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-16T19:29:11.126+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-16T19:29:21.479+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-16T19:29:21.484+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-16T19:29:21.495+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-16T19:29:21.498+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-16T19:29:21.501+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-16T19:29:21.506+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-16T19:29:21.509+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-16T19:29:25.025+08:00 [wecom] v1.0.13 loaded
2026-04-16T19:29:25.031+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-16T19:29:25.069+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-16T19:29:25.109+08:00 [heartbeat] started
2026-04-16T19:29:25.112+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-16T19:29:25.116+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-16T19:29:25.117+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 6928)
2026-04-16T19:29:25.119+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-16.log
2026-04-16T19:29:25.183+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
[GatewayManager] Optimization post-ready: warmupSpawned=true pid=11608 cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Startup phase: compile-cache warmup spawn took 68ms
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=62387 compileCache=true warmup=true
2026-04-16T19:29:25.620+08:00 [ws] webchat connected conn=70873d0d-c79c-4268-91f3-5bbe1fd8afec remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-16T19:29:30.162+08:00 [ws] ⇄ res ✓ config.get 4517ms conn=70873d0d…afec id=a9af02cc…e83b
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 18ms
[GatewayManager] Startup phase: sanitize openclaw config took 1104ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=1, elapsedMs=10631, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 10635ms
[GatewayManager] Startup phase: ensure builtin skills took 104ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 2ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 1305ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 340ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 746ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 4ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 1ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 145ms
[GatewayManager] Startup phase: patch gateway runtime took 2561ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-16T21:06:30.643+08:00 [gateway] force: no listeners on port 18789
2026-04-16T21:06:30.685+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-16T21:06:30.755+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 bbdb6ec7d5375d3418a90c0fcc1bb6f9e4baf032561673f9a512ca2a8662acc5 -> dbad2695ccf6162b607030bbaff7e27e124f41da8adb71c1df81e90dd3a439e7, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-16T21:06:30.762+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-16T21:06:30.778+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-16T21:06:57.531+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-16T21:07:06.352+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-16T21:07:06.356+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-16T21:07:06.367+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-16T21:07:06.371+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-16T21:07:06.374+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-16T21:07:06.378+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-16T21:07:06.381+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-16T21:07:10.035+08:00 [wecom] v1.0.13 loaded
2026-04-16T21:07:10.041+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-16T21:07:10.087+08:00 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-16T21:07:10.125+08:00 [heartbeat] started
2026-04-16T21:07:10.130+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-16T21:07:10.136+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-16T21:07:10.139+08:00 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 11456)
2026-04-16T21:07:10.143+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-16.log
[GatewayManager] Optimization post-ready: warmupSpawned=true pid=3768 cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Startup phase: compile-cache warmup spawn took 70ms
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=44403 compileCache=true warmup=true
2026-04-16T21:07:10.217+08:00 [browser/server] Browser control listening on http://127.0.0.1:18791/ (auth=token)
2026-04-16T21:07:10.434+08:00 [ws] webchat connected conn=d44cd5d3-0d32-4777-babf-7519cfaba159 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-16T21:07:12.788+08:00 [ws] ⇄ res ✓ config.get 2335ms conn=d44cd5d3…a159 id=c2e73bd1…066b
2026-04-16T22:04:33.011+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T22:04:33.023+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-16T23:04:33.010+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-16T23:04:33.015+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-17T00:04:33.006+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-17T00:04:33.012+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-17T01:04:33.040+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-17T01:04:33.046+08:00 [reload] config hot reload applied (models.providers.zai.models)
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 5ms
[GatewayManager] Startup phase: sanitize openclaw config took 18ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=4369, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 4372ms
[GatewayManager] Startup phase: ensure builtin skills took 78ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 3ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 751ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 1ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 203ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 452ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 121ms
[GatewayManager] Startup phase: patch gateway runtime took 1547ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-24T20:47:20.314+08:00 [gateway] force: no listeners on port 18790
2026-04-24T20:47:20.357+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T20:47:20.407+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 7331c90b3141f142effe3d6c7e08bbba4cdd88ba82cf7d8926b6559ae4c01537 -> 2f7b4cf2cab58517b971489f27fdb53c134b5690a6e1b2cf6e5cd1a836857d80, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-24T20:47:20.413+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-24T20:47:20.425+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T20:47:37.024+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T20:47:43.542+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-24T20:47:43.545+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-24T20:47:43.551+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-24T20:47:43.552+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-24T20:47:43.554+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-24T20:47:43.557+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-24T20:47:43.560+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-24T20:47:45.801+08:00 [wecom] v1.0.13 loaded
2026-04-24T20:47:45.804+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-24T20:47:45.834+08:00 [canvas] host mounted at http://127.0.0.1:18790/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-24T20:47:45.858+08:00 [heartbeat] started
2026-04-24T20:47:45.861+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-24T20:47:45.865+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-24T20:47:45.867+08:00 [gateway] listening on ws://127.0.0.1:18790, ws://[::1]:18790 (PID 84464)
2026-04-24T20:47:45.870+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-24.log
2026-04-24T20:47:45.918+08:00 [browser/server] Browser control listening on http://127.0.0.1:18792/ (auth=token)
[GatewayManager] Optimization post-ready: warmupSpawned=true pid=82596 cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Startup phase: compile-cache warmup spawn took 97ms
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=28527 compileCache=true warmup=true
2026-04-24T20:47:46.341+08:00 [ws] webchat connected conn=9bf662d9-f1b0-4782-8201-8fba9da53117 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-24T20:47:49.394+08:00 [ws] ⇄ res ✓ config.get 3035ms conn=9bf662d9…3117 id=ee517f9f…d415
2026-04-24T21:46:55.254+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-24T21:46:55.261+08:00 [reload] config hot reload applied (models.providers.zai.models)
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 3ms
[GatewayManager] Startup phase: sanitize openclaw config took 7ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=2709, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 2711ms
[GatewayManager] Startup phase: ensure builtin skills took 14ms
[GatewayManager] Startup phase: ensure skill path guidance took 0ms
[GatewayManager] Startup phase: pre-register device took 0ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 1ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 459ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 247ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 485ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 108ms
[GatewayManager] Startup phase: patch gateway runtime took 1312ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-24T22:03:05.519+08:00 [gateway] force: no listeners on port 18790
2026-04-24T22:03:05.592+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:03:05.606+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 436ab9191ce5251ad0e92d63eeef16dd583e87979e8392f350673974f8f36f4f -> d9b733a66dbcb27b85aae2970ae77f47cee3f922d92986d048beafd53b1eb97c, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-24T22:03:05.610+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-24T22:03:05.620+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:03:10.897+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:03:11.701+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-24T22:03:11.704+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-24T22:03:11.712+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-24T22:03:11.717+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-24T22:03:11.720+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-24T22:03:11.725+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-24T22:03:11.729+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-24T22:03:13.437+08:00 [wecom] v1.0.13 loaded
2026-04-24T22:03:13.441+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-24T22:03:13.466+08:00 [canvas] host mounted at http://127.0.0.1:18790/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-24T22:03:13.488+08:00 [heartbeat] started
2026-04-24T22:03:13.491+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-24T22:03:13.495+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-24T22:03:13.500+08:00 [gateway] listening on ws://127.0.0.1:18790, ws://[::1]:18790 (PID 106212)
2026-04-24T22:03:13.511+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-24.log
2026-04-24T22:03:13.571+08:00 [browser/server] Browser control listening on http://127.0.0.1:18792/ (auth=token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=10741 compileCache=true warmup=true
2026-04-24T22:03:13.631+08:00 [ws] webchat connected conn=6e64eac5-6e6a-4795-aff1-aa87a952e676 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-24T22:03:15.746+08:00 [ws] ⇄ res ✓ config.get 1970ms conn=6e64eac5…e676 id=812d11e1…3ad8
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 5ms
[GatewayManager] Startup phase: sanitize openclaw config took 8ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=2746, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 2748ms
[GatewayManager] Startup phase: ensure builtin skills took 13ms
[GatewayManager] Startup phase: ensure skill path guidance took 0ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 1ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 1ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 446ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 213ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 493ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 1ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 117ms
[GatewayManager] Startup phase: patch gateway runtime took 1285ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-24T22:29:01.231+08:00 [gateway] force: no listeners on port 18790
2026-04-24T22:29:01.303+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:29:01.317+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 7080ca551d87a60a52f4879da8c9fa78108b910f8ad8046dc572baecb1906779 -> 9ee1f4d95397dd2e946504fc0715dc2ff2bcad5b760b0481e0f7a67624e21640, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-24T22:29:01.322+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-24T22:29:01.332+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:29:06.654+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:29:07.526+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-24T22:29:07.532+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-24T22:29:07.546+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-24T22:29:07.550+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-24T22:29:07.554+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-24T22:29:07.559+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-24T22:29:07.562+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-24T22:29:09.549+08:00 [wecom] v1.0.13 loaded
2026-04-24T22:29:09.553+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-24T22:29:09.584+08:00 [canvas] host mounted at http://127.0.0.1:18790/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-24T22:29:09.608+08:00 [heartbeat] started
2026-04-24T22:29:09.612+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-24T22:29:09.617+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-24T22:29:09.619+08:00 [gateway] listening on ws://127.0.0.1:18790, ws://[::1]:18790 (PID 114676)
2026-04-24T22:29:09.623+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-24.log
2026-04-24T22:29:09.671+08:00 [browser/server] Browser control listening on http://127.0.0.1:18792/ (auth=token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=11259 compileCache=true warmup=true
2026-04-24T22:29:09.825+08:00 [ws] webchat connected conn=1d473ba4-cbf0-4350-8cb2-4c4c33ba9e4e remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-24T22:29:12.187+08:00 [ws] ⇄ res ✓ config.get 2196ms conn=1d473ba4…9e4e id=3d0957f0…8202
EXIT
[GatewayManager] Startup phase: prepare runtime took 1ms
[GatewayManager] Startup phase: sync settings catalog took 3ms
[GatewayManager] Startup phase: sanitize openclaw config took 7ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=2715, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 2717ms
[GatewayManager] Startup phase: ensure builtin skills took 13ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 471ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 225ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 465ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 1ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 116ms
[GatewayManager] Startup phase: patch gateway runtime took 1293ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-24T22:31:14.280+08:00 [gateway] force: no listeners on port 18790
2026-04-24T22:31:14.354+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:31:14.368+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 4e39c4aa4c1e3df07aec4053997f4d3589d0a03f2288a646b7b2f8033300ebfa -> 7461de4101edcf0af3c9dfea3130f4f69dab1229d88a0bd6adb9508fc030013a, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-24T22:31:14.373+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-24T22:31:14.384+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:31:19.803+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:31:20.729+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-24T22:31:20.732+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-24T22:31:20.742+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-24T22:31:20.745+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-24T22:31:20.747+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-24T22:31:20.752+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-24T22:31:20.755+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-24T22:31:22.649+08:00 [wecom] v1.0.13 loaded
2026-04-24T22:31:22.653+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-24T22:31:22.683+08:00 [canvas] host mounted at http://127.0.0.1:18790/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-24T22:31:22.708+08:00 [heartbeat] started
2026-04-24T22:31:22.711+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-24T22:31:22.715+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-24T22:31:22.718+08:00 [gateway] listening on ws://127.0.0.1:18790, ws://[::1]:18790 (PID 111448)
2026-04-24T22:31:22.722+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-24.log
2026-04-24T22:31:22.775+08:00 [browser/server] Browser control listening on http://127.0.0.1:18792/ (auth=token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=11252 compileCache=true warmup=true
2026-04-24T22:31:22.826+08:00 [ws] webchat connected conn=051a7ee0-5e86-4460-a786-d05e186e80ee remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-24T22:31:25.140+08:00 [ws] ⇄ res ✓ config.get 2119ms conn=051a7ee0…80ee id=f2c71b9a…baca
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 4ms
[GatewayManager] Startup phase: sanitize openclaw config took 8ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=3302, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 3304ms
[GatewayManager] Startup phase: ensure builtin skills took 18ms
[GatewayManager] Startup phase: ensure skill path guidance took 0ms
[GatewayManager] Startup phase: pre-register device took 0ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 2ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 1ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 562ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 235ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 511ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 2ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 134ms
[GatewayManager] Startup phase: patch gateway runtime took 1462ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-24T22:34:17.779+08:00 [gateway] force: no listeners on port 18790
2026-04-24T22:34:17.858+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:34:17.873+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 2254be3f1a87c120c1f1277f50ebc1afe3d2914ad8623a23cd62659a560f03e2 -> 836abc3239ddff29613516087c0520744d6270967d0e8335361c95d2de407511, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-24T22:34:17.878+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-24T22:34:17.888+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:34:23.474+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:34:24.275+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-24T22:34:24.278+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-24T22:34:24.285+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-24T22:34:24.287+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-24T22:34:24.289+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-24T22:34:24.292+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-24T22:34:24.294+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-24T22:34:25.957+08:00 [wecom] v1.0.13 loaded
2026-04-24T22:34:25.960+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-24T22:34:25.989+08:00 [canvas] host mounted at http://127.0.0.1:18790/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-24T22:34:26.015+08:00 [heartbeat] started
2026-04-24T22:34:26.021+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-24T22:34:26.027+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-24T22:34:26.030+08:00 [gateway] listening on ws://127.0.0.1:18790, ws://[::1]:18790 (PID 115408)
2026-04-24T22:34:26.033+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-24.log
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=11267 compileCache=true warmup=true
2026-04-24T22:34:26.105+08:00 [browser/server] Chrome extension relay init failed for profile "chrome": Error: listen EADDRINUSE: address already in use 127.0.0.1:18793
2026-04-24T22:34:26.107+08:00 [browser/server] Browser control listening on http://127.0.0.1:18792/ (auth=token)
2026-04-24T22:34:26.120+08:00 [ws] webchat connected conn=b130eb02-6ede-48d2-9e4a-73ab274cd270 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-24T22:34:28.250+08:00 [ws] ⇄ res ✓ config.get 1980ms conn=b130eb02…d270 id=ce0529cf…5069
EXIT
[GatewayManager] Startup phase: prepare runtime took 0ms
[GatewayManager] Startup phase: sync settings catalog took 5ms
[GatewayManager] Startup phase: sanitize openclaw config took 9ms
[GatewayManager] Config validation setup: entry=C:\Users\Administrator\.openclaw-autoclaw\gateway-launcher.cjs, compileCache=true, cacheDir=C:\Users\Administrator\.openclaw-autoclaw\.compile-cache
[GatewayManager] Config validation round 0: status=0, elapsedMs=3262, timedOut=false
[GatewayManager] Startup phase: validate and fix config took 3263ms
[GatewayManager] Startup phase: ensure builtin skills took 77ms
[GatewayManager] Startup phase: ensure skill path guidance took 1ms
[GatewayManager] Startup phase: pre-register device took 1ms
[GatewayManager] Runtime patch step: patchPiAiModelsBaseUrl took 1ms
[GatewayManager] Runtime patch step: removeBuiltinZaiModels took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestId took 0ms
[GatewayManager] Runtime patch step: patchEmbeddedPiAgentSessionContext took 514ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionHeader took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsRequestTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsSessionTrace took 0ms
[GatewayManager] Runtime patch step: patchOpenAICompletionsModelPrefix took 0ms
[GatewayManager] Runtime patch step: patchGatewayDistModelIdentity took 221ms
[GatewayManager] Runtime patch step: patchFsSafeDirectoryHandling took 501ms
[GatewayManager] Runtime patch step: patchWindowsPortForceHandling took 2ms
[GatewayManager] Runtime patch step: injectRemoteVisionModelsIntoPiAi took 0ms
[GatewayManager] Runtime patch step: patchPiAiModelsAuthHeader took 1ms
[GatewayManager] Runtime patch step: validateGatewayRuntimePatch took 125ms
[GatewayManager] Startup phase: patch gateway runtime took 1375ms
[gateway-launcher] loading E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
[gateway-launcher] load ok: E:\AutoClaw\resources\gateway\openclaw\gateway-bundle.mjs
|
o  Doctor changes --------------------------------------+
|                                                       |
|  qwen-portal auth configured, enabled automatically.  |
|                                                       |
+-------------------------------------------------------+
|
o  Doctor warnings --------------------------------------------------------+
|                                                                          |
|  - channels.openclaw-weixin: accounts.default is missing and no valid    |
|    account-scoped binding exists for configured accounts                 |
|    (9af714449ec4-im-bot). Channel-only bindings (no accountId) match     |
|    only default. Add bindings[].match.accountId for one of these         |
|    accounts (or "*"), or add channels.openclaw-weixin.accounts.default.  |
|                                                                          |
+--------------------------------------------------------------------------+
|
o  Doctor ----------------------------------------------+
|                                                       |
|  Run "openclaw doctor --fix" to apply these changes.  |
|                                                       |
+-------------------------------------------------------+
2026-04-24T22:37:28.978+08:00 [gateway] force: no listeners on port 18790
2026-04-24T22:37:29.050+08:00 Config warnings:
- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:37:29.063+08:00 Config overwrite: C:\Users\Administrator\.openclaw-autoclaw\openclaw.json (sha256 04789bf89dfa6b415fedddff8f88353852a93de2ee68fb0a9b63d60f0913418d -> 8045559bca03594c7eba0aa6d6222320774e80877d4bea52e94dc45d9b5c3355, backup=C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak)
2026-04-24T22:37:29.068+08:00 [gateway] auto-enabled plugins:
- qwen-portal auth configured, enabled automatically.
2026-04-24T22:37:29.078+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:37:34.639+08:00 Config warnings:\n- plugins.entries.qwen-portal-auth: plugin not found: qwen-portal-auth (stale config entry ignored; remove it from plugins config)
2026-04-24T22:37:35.535+08:00 [gateway] feishu_chat: Registered feishu_chat, feishu_chat_members
2026-04-24T22:37:35.539+08:00 [gateway] feishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages
2026-04-24T22:37:35.548+08:00 [gateway] feishu_im_bot_image: Registered feishu_im_bot_image tool
2026-04-24T22:37:35.550+08:00 [gateway] feishu_im: Registered feishu_im_bot_image
2026-04-24T22:37:35.552+08:00 [gateway] Registered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)
2026-04-24T22:37:35.558+08:00 [gateway] feishu_oauth: Registered feishu_oauth tool
2026-04-24T22:37:35.566+08:00 [gateway] feishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool
2026-04-24T22:37:37.571+08:00 [wecom] v1.0.13 loaded
2026-04-24T22:37:37.576+08:00 [gateway] [plugins] plugin id mismatch (config uses "wecom", export uses "wecom-openclaw-plugin") (plugin=wecom, source=E:\AutoClaw\resources\gateway\openclaw\extensions\wecom\dist\index.esm.js)
2026-04-24T22:37:37.602+08:00 [canvas] host mounted at http://127.0.0.1:18790/__openclaw__/canvas/ (root C:\Users\Administrator\.openclaw-autoclaw\canvas)
2026-04-24T22:37:37.625+08:00 [heartbeat] started
2026-04-24T22:37:37.628+08:00 [health-monitor] started (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
2026-04-24T22:37:37.632+08:00 [gateway] agent model: zai/huawei_glm-5
2026-04-24T22:37:37.634+08:00 [gateway] listening on ws://127.0.0.1:18790, ws://[::1]:18790 (PID 113280)
2026-04-24T22:37:37.637+08:00 [gateway] log file: \tmp\openclaw\openclaw-2026-04-24.log
2026-04-24T22:37:37.681+08:00 [browser/server] Browser control listening on http://127.0.0.1:18792/ (auth=token)
[GatewayManager] Optimization summary: bundleHit=true fallback=false readyMs=11745 compileCache=true warmup=true
2026-04-24T22:37:38.025+08:00 [ws] webchat connected conn=7f13955c-ee20-4479-bad7-a8c61adda7d0 remote=127.0.0.1 client=AutoClaw webchat v0.1.13
2026-04-24T22:37:40.225+08:00 [ws] ⇄ res ✓ config.get 2039ms conn=7f13955c…a7d0 id=c65facd6…ae42
2026-04-24T22:46:55.278+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-24T22:46:55.281+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-24T23:46:55.272+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-24T23:46:55.276+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T00:46:55.289+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T00:46:55.292+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T01:46:55.292+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T01:46:55.295+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T02:47:00.339+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T02:47:00.342+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T03:47:00.354+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T03:47:00.357+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T04:47:00.359+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T04:47:00.362+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T05:47:00.365+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T05:47:00.370+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T06:47:00.408+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T06:47:00.412+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T07:47:00.401+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T07:47:00.404+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T08:47:00.428+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T08:47:00.432+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T09:47:00.399+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T09:47:00.405+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T10:47:00.422+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T10:47:00.425+08:00 [reload] config hot reload applied (models.providers.zai.models)
2026-04-25T11:47:01.849+08:00 [reload] config change detected; evaluating reload (models.providers.zai.models)
2026-04-25T11:47:01.854+08:00 [reload] config hot reload applied (models.providers.zai.models)
EXIT

```
