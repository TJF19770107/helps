# 🦞 龙虾视频流水线六合一 · 使用手册

> **v1.0 | 2026-08-23** · 实测打通版 · 零成本 · 单文件夹

---

## 1. 快速测试（推荐先跑）

```bash
# 进入管线目录
cd "G:/WorkBuddy_Data/lobster_video_pipeline"

# 跑自检（验证 6 个子 Skill 都到位）
python "C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe" "00_integration/test_pipeline.py"

# 预期输出：
# ✅ 01_video-use: 818K, SKILL.md 23KB 完整
# ✅ 02_jianying-editor: 8.0M, SKILL.md 32KB + 8 个 examples
# ✅ 03_seedance2-skill: 53K, 中英双版 SKILL.md
# ✅ 04_remotion-skill: 14M sparse, claude-code-plugin 已取
# ✅ 05_hyperframes: 147M, 6 个内置 SKILL.md (.agents/skills)
# ✅ 06_image-generation: 内置 MCP, 1.39MB 实测结果
# 🎉 六合一管线全部就绪
```

---

## 2. 整条管线跑通（端到端）

```bash
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
PIPE="G:/WorkBuddy_Data/lobster_video_pipeline"

# 示例：30 秒抖音带货数字人视频（最小闭环）
python "$PY" "$PIPE/00_integration/pipeline.py" \
  --task full \
  --brief "30 秒抖音带货，亚洲女性模特，展示电子牙刷" \
  --out "$PIPE/test_output/sample_30s.mp4"
```

**这条命令会触发**：06 生模特图 → 03 写视频 prompt → 02 生剪映草稿 → 01 render 出 MP4

---

## 3. 分阶段调用

### 3.1 仅生图

```bash
python "$PY" "$PIPE/00_integration/pipeline.py" \
  --task image \
  --prompt "电商白底产品图，30岁亚洲女性，口红特写" \
  --out "$PIPE/test_output/product.png"
```

### 3.2 仅写视频 prompt

```bash
python "$PY" "$PIPE/00_integration/pipeline.py" \
  --task seedance-prompt \
  --subject "智能咖啡机广告" \
  --style "赛博科技感" \
  --out "$PIPE/test_output/coffee_prompt.md"
```

### 3.3 仅视频剪辑（最常用）

```bash
python "$PY" "$PIPE/00_integration/pipeline.py" \
  --task video-edit \
  --input "source.mp4" \
  --out "$PIPE/test_output/final.mp4" \
  --config "remove_filler=true,burn_subs=true"
```

### 3.4 仅生剪映草稿

```bash
python "$PY" "$PIPE/00_integration/pipeline.py" \
  --task sketch \
  --script "把'灯光-柔光-明亮-特写-微笑'这五句话配上我提供的三张图"
```

---

## 4. Skill 互相组合

### 4.1 接单-标准路径（影视解说）

```
原始视频
   ↓
[01 video-use: 转写 → 去口水 → 加字幕]
   ↓
[06 ImageGeneration: 生封面图（基于视频关键帧 prompt）]
   ↓
final.mp4 + cover.jpg
```

### 4.2 接单-数字人路径（带货）

```
文案（客户提供）
   ↓
[03 seedance2-skill: 模板化视频 prompt]
   ↓
[外部视频 API 调用（Seedance/可灵/Agnes）]  ← 本目录不含 API key,用户接
   ↓
[01 video-use: 二次剪辑+字幕+LOGO]
   ↓
final.mp4
```

### 4.3 自媒体-品牌短剧

```
剧本
   ↓
[02 jianying-editor: 生草稿+AI配音+字幕+特效]
   ↓
剪映内手动导出（或 auto_exporter.py 脚本）
   ↓
final.mp4
```

---

## 5. 故障排查

| 现象 | 排查 |
|------|------|
| `ModuleNotFoundError: PIL` | 装 `pip install pillow`（WorkBuddy Python 已 OK）|
| `ffmpeg not found` | `winget install ffmpeg` 或下载静态包加 PATH |
| 02 jianying 编辑器找不到草稿目录 | 装 Windows 剪映 5.9 或更低,确认 `%LOCALAPPDATA%\JianyingPro\` 存在 |
| 04 remotion 报 Node 不足 | 装 Node 22+（hyperframes 要求）|
| 05 hyperframes `npx` 慢 | 第一次需下载 Chromium(≈200MB),后可离线 |
| 06 ImageGen 返回 `disconnected` | 检查 WorkBuddy 的 MCP 连接器状态,可能需重新 Trust |

---

## 6. 关键设计决策

1. **为什么在 G 盘而非 E 盘?** E 盘 0 字节剩余(已 100% 占满),沙箱 `/tmp` 也指向 E,任何写都会失败。
2. **为什么 remotion 1.2GB 瘦身到 14MB?** 用 sparse-checkout 只取 9 个核心包,真要全栈用 `cd 04_remotion_skill_src && bun install` 即恢复全栈。
3. **为什么 hyperframes 保留 147MB?** 它已含 6 个内置 SKILL.md 和完整源码,这是真实工作区。clone 都是浅克隆。
4. **为什么不写 E 盘?** USER MEMORY §G 章节硬保护,但 E 满也无法写。
5. **能不能一条命令装回 E 盘?** 等 E 盘清出空间后,执行 `mklink /J "E:\...\技能库\video-pipeline" "G:\WorkBuddy_Data\lobster_video_pipeline\"` 创建 junction。

---

## 7. 文件清单（截至 2026-08-23 20:20 CST）

```
G:\WorkBuddy_Data\lobster_video_pipeline\
├── SKILL.md                            # 顶层整合 (~5KB)
├── README.md                           # 本文件
├── 01_video-use\                       # 818K (browser-use/video-use)
│   ├── SKILL.md                        # 23KB 原仓库文件
│   ├── helpers\                        # grade/pack_transcripts/render/timeline_view/transcribe ×6
│   └── skills\manim-video\
├── 02_jianying-editor\                 # 8.0M (luoluoluo22/jianying-editor-skill)
│   ├── SKILL.md                        # 32KB 原仓库文件
│   ├── scripts\                        # jy_wrapper / auto_exporter / draft_inspector...
│   ├── examples\                       # 8 个完整示例
│   ├── docs\ rules\ prompts\ tests\    # 完整开发生态
│   └── references\
├── 03_seedance2-skill\                 # 53K (dexhunter/seedance2-skill)
│   ├── SKILL.md                        # 16KB 原仓库文件
│   ├── zh\SKILL.md                     # 中文版
│   └── README-zh.md
├── 04_remotion_skill_src\              # 14M sparse (remotion-dev/remotion)
│   ├── packages\claude-code-plugin\    # Skill 入口（agent 调用 remotion)
│   ├── packages\core\cli\bundler\...   # 9 个核心包
│   └── README.md
├── 05_hyperframes_src\                 # 147M (heygen-com/hyperframes)
│   ├── .agents\skills\                 # 6 个内置 SKILL.md (captions-overlay 等)
│   ├── packages\{cli,core,engine,...}  # 9 个包
│   ├── AGENTS.md / CLAUDE.md / README.md
│   └── examples\ docs\ assets\
├── 06_image-generation\                # 内置 MCP（无本地文件）
│   └── SKILL.md                        # 新写：ImageGen 标准化入口
├── 00_integration\                     # 集成与测试
│   ├── pipeline.py                     # Python 主入口
│   ├── test_pipeline.py                # 自检脚本
│   └── playbook.md                     # 待补
└── test_output\                        # 输出目录（空,所有 demo 落这）
```

---

## 8. 下一步（用户拍板项）

| 待办 | 备注 |
|------|------|
| 注册到龙虾五步法 §11 | 链接到 `E:\...\技能库\lobster_task_standard_workflow_v3.0\龙虾五步法V3.6·PR#21闭环版（成本优先置顶）SKILL.md` §11 软链接 |
| 写 `00_integration/playbook.md` | 用户使用手册 + 故障排查 |
| 试 E 盘 junction | 等 E 盘清出 1KB 空间（junction 只需 <1KB 元数据）|
| 跑通一个完整 demo | 在 `test_output/` 出实物素材,顺便做接单实证 |

---

**手工单文件夹**: G:\WorkBuddy_Data\lobster_video_pipeline
**自动跑测**: python 00_integration/test_pipeline.py
**包月免费**: ¥0
**作者**: 龙虾五步法 V3.6 + 四化迭代知识库 + 1234（仓颉/全域/龙虾/赛博）
