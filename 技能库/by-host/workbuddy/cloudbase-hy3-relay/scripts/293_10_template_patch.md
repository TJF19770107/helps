# 全域模板 #293 回填补丁 — 新增 §293.10

> 本文件为可直接合并进「龙虾全域官方模板-最终版.md」的章节片段。
> **插入位置**：在 `### 293.9 技能注册` 之后、`### v3.112 更新记录` 之前。
> **受管文件**：`E:/龙虾AI主控中心/我的AI分身/技能库/龙虾全域官方模板-最终版.md`
> 该文件属沙箱禁止写入的受管目录，须由用户在本机（沙箱外）以编辑器 / VS Code 粘贴本节内容。

---

### 293.10 受管目录放行与技能镜像标准流程（2026-07-22 补充）

> 背景：第三方免费额度接入（#293.8）落地后，技能需同步至舰队共享 `技能库/`（受管目录）。本流程规范「沙箱受管目录放行 + 技能镜像」的标准做法，避免 Agent 静默写受管文件或被拦截后无据可循。

#### 293.10.1 触发场景
- 需将用户级技能（`~/.workbuddy/skills/<skill>/`）镜像到舰队共享 `技能库/`；
- 需回填 / 修改全域模板、AGENTS.md 等**受管文件**；
- Agent 报 `Blocked paths: ...` 或 `SANDBOX EXECUTION REJECTED BY USER` 时。

#### 293.10.2 沙箱文件系统隔离原理
| 误区 | 正解 |
|------|------|
| 存在 `sandbox.allowedPaths` / `sandbox.deniedPaths` | ❌ 不存在；放行靠 `permissions` 配置 |
| `permissions.deny` 之外随便写 | ❌ 沙箱默认只许写当前工作目录及其子目录，目录外被 OS 级拦截 |
| Agent 在沙箱内改 `settings.json` | ❌ `settings.json` 自身受写保护（防逃逸），只能用户在沙箱外改 |
| `~/.workbuddy/skills/` 需放行 | ❌ 用户级技能目录已在可写范围，无需额外放行 |

#### 293.10.3 放行配置（settings.json 补丁）
```json
{
  "permissions": {
    "additionalDirectories": ["E:/龙虾AI主控中心/我的AI分身/技能库/"],
    "allow": ["Edit(E:/龙虾AI主控中心/我的AI分身/技能库/**)"]
  }
}
```
- 位置：用户级 `C:\Users\Administrator\.workbuddy\settings.json`（或 `~/.codebuddy/settings.json`）；项目级 `<项目根>\.workbuddy\settings.json`。
- 修改须在**沙箱外**完成（编辑器 / VS Code / WorkBuddy `/config` 面板）；改完重启生效。
- 交互式放行：下次弹窗选「永久更新配置」即自动写入 `allow` 规则。

#### 293.10.4 镜像技能标准流程
1. **备份**：镜像前备份现有共享版本（时间戳目录 `.bak_<skill>_<ts>`），支持回滚；
2. **镜像**：`Copy-Item -Recurse <用户级技能> <共享技能库>/<skill>`；
3. **校验**：文件数一致 + MD5 抽样 + 目录结构比对；
4. **触发语**：用户在对话说「镜像技能」即可由 Agent 自动执行（放行后零手工）。

#### 293.10.5 安全约束（P0）
1. **最小权限**：只放行 `技能库/` 单目录，禁整盘 `E:/` 放行；
2. **Windows WebDAV 风险**：勿启用 WebDAV、勿让 Agent 访问 `\\*` 路径（可绕过权限系统）；
3. **deny 优先**：若 `permissions.deny` 含覆盖规则需先移除；
4. **配置文件受保护是安全特性**：`settings.json` 写保护防提示注入逃逸，手动改即可。

#### 293.10.6 关联交付物
- 落地案例技能：`技能库/cloudbase-hy3-relay/`（第七节）
- 补丁脚本：`settings_permission_patch.json` / `mirror_skill.ps1` / `293_10_template_patch.md`

#### 293.10.7 代理式指令编写约束（v3.120 · 2026-07-22 追加）
> 背景：本次「技能镜像与全域模板回填自动化」代理式指令在沙箱内执行时，暴露两条结构性冲突。凡编写「交给 Agent 全自动执行」的指令，必须遵守：

1. **标准件路径以受管目录为唯一真源**：指令中引用的标准件 / 模板 / 技能，其权威路径一律以 `E:/龙虾AI主控中心/我的AI分身/技能库/` 下**既有文件**为准；**用户级 `~/.workbuddy/skills/` 副本通常不存在**，勿在指令里假定其存在。Agent 读取标准件应直接读 `E:/.../技能库/` 受管路径（只读可），而非用户级副本。
2. **受管目录写必须预设「产出补丁 + 外部执行」分支**：凡指令涉及写入受管目录（`技能库/`、`Obsidian知识库/`、`龙虾全域官方模板-最终版.md` 等），Agent **不得假定可直写**——沙箱会硬拦截（`Blocked paths` / `SANDBOX EXECUTION REJECTED BY USER`）。指令应明确要求 Agent：**自动生成完整补丁文件 + 一键执行脚本（置于用户级可写目录），并提示用户在沙箱外执行**，而非要求 Agent 在沙箱内完成该写操作。
   - 违例后果：假定直写 → 要么被拦截导致任务卡死，要么被迫重试受管目录（违反 no-retry 铁律）；二者皆不可取。

#### 293.10.8 指令标准化校验子技能注册（lobster_prompt_authoring v1.0 · v3.121）
> 配套落地：将 §293.10.7 两条铁律固化为独立技能包，凡构建跨 Agent 代理指令时自动加载校验。

- **技能标识**：`lobster_prompt_authoring`
- **绑定**：全域模板 §293.10.7（v3.120）
- **定位**：指令标准化校验子技能（所有向外下发 WorkBuddy / Codex / Hermes / Marvis 代理指令时自动加载）
- **完整正文**：随附独立技能文件 `lobster_prompt_authoring.md`（含两条强制约束、调用触发规则、违规拦截规则）
- **注册方式（受管写，走补丁+外部执行分支）**：
  - 落点：`E:/龙虾AI主控中心/我的AI分身/技能库/lobster_prompt_authoring.md`
  - 该路径属受管目录，Agent **禁止沙箱内直写**；提供一键脚本（UTF-8 BOM）由用户在沙箱外运行生成：
    ```powershell
    $filePath = "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_prompt_authoring.md"
    $content = @'
    # lobster_prompt_authoring 代理指令编写规范技能 v1.0
    绑定全域模板 §293.10.7（v3.120）
    ...（完整正文见随附技能文件 lobster_prompt_authoring.md）
    '@
    [System.IO.File]::WriteAllText($filePath, $content, [System.Text.Encoding]::UTF8)
    Write-Host "技能文件创建完成"
    ```
- **全域模板【技能自动加载清单】追加行**（在对应清单节追加）：
  > 当构建跨 Agent 代理指令（生成给 WorkBuddy / Codex / Hermes / Marvis 的自动化指令、制作模板补丁、修订技能文档）时，自动载入技能：`lobster_prompt_authoring`

---

### v3.112 更新记录（追加行）

| 版本 | 日期 | 变更 |
|------|------|------|
| v3.119 | 2026-07-22 | +#293.10 受管目录放行与技能镜像标准流程(沙箱放行+技能镜像) |
| v3.120 | 2026-07-22 | +#293.10.7 代理式指令编写约束(标准件路径唯一真源+受管目录写预设补丁/外部执行分支) |
| v3.121 | 2026-07-22 | +#293.10.8 注册指令标准化校验子技能 lobster_prompt_authoring v1.0(绑定§293.10.7) |
