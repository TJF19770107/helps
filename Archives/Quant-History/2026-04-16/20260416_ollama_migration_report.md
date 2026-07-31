# Ollama迁移与离线验证执行日志

- 时间: 2026-04-16
- 执行目录: `E:\龙虾AI主控中心`
- 目标: 迁移Ollama目录到`E:\.ollama`、清理`AppData\Local\Ollama`缓存、对齐本地离线推理

## 执行结果摘要

- 目录扫描结果:
  - `C:\Users\Administrator\AppData\Local\Ollama` 存在，约 `0.005 GB`
  - `C:\Users\Administrator\AppData\Local\Programs\Ollama` 存在，约 `5.881 GB`
  - `C:\Users\Administrator\.ollama` 不存在
  - `C:\ProgramData\Ollama` 不存在
  - `E:\.ollama` 不存在
- 模型清单核验:
  - `E:\.ollama\models\manifests` 不存在
  - `C:\Users\Administrator\AppData\Local\Programs\Ollama\models\manifests` 不存在
  - `C:\Users\Administrator\AppData\Local\Ollama\models\manifests` 不存在
  - 结论: 未发现 `qwen2.5` 本地模型清单，无法完成“离线模型可用”验证
- 环境变量已设置(机器级):
  - `OLLAMA_HOME=E:\.ollama`
  - `OLLAMA_AUTO_UPDATE=false`
  - `OLLAMA_MODELS_AUTO_PULL=false`
- 当前C盘剩余空间:
  - `FreeGB=1.57`

## 阻塞与风险

- 关键阻塞:
  - 本机未发现任何可用的Ollama模型仓库目录(`.ollama/models/manifests`)
  - 在未联网且无离线备份前提下，无法验证`qwen2.5:3b`推理
- 迁移风险说明:
  - `Programs\Ollama`属于安装目录，复制到`E:\.ollama`并不能替代模型仓库
  - 若直接删除C盘安装目录，可能导致客户端损坏

## 后续操作建议（离线优先）

- 从旧机器或备份介质离线拷贝完整`.ollama`到`E:\.ollama`
- 拷贝完成后运行:
  - `E:\龙虾AI主控中心\龙虾远程控制包\本地推理自检_Ollama_离线.bat`
- 若必须释放C盘:
  - 仅清理`C:\Users\Administrator\AppData\Local\Ollama`中的`updates/updates_v2/*.log`
  - 不删除`C:\Users\Administrator\AppData\Local\Programs\Ollama`

## 二次验证（固定路径执行）

- 固定清单路径（用户指定）:
  - `E:\Ollama\models\manifests\registry.ollama.ai\library\`
- 清单核验结果:
  - `deepseek-r1` 存在，标签文件: `1.5b, 7b`
  - `qwen2.5` 存在，标签文件: `3b, 7b-instruct`
  - `qwen3` 存在，标签文件: `8b`
  - `qwen3.5` 存在，标签文件: `2b`
- 环境变量修正结果（机器级）:
  - `OLLAMA_HOME=E:\Ollama`（已生效）
  - `OLLAMA_AUTO_UPDATE=false`（已生效）
  - `OLLAMA_MODELS_AUTO_PULL=false`（已生效）
- 本地推理命令验证:
  - 执行: `ollama run qwen2.5:3b "请输出一段不超过100字的测试文本，仅输出正文。"`
  - 结果: 用户本机管理员PowerShell终端执行成功（无联网拉取行为提示）
  - 输出样例:
    - `Qwen在这里随时准备帮助你，无论你需要什么信息或是完成什么样的任务。`
- C盘最小风险清理状态:
  - 目标路径 `C:\Users\Administrator\AppData\Local\Ollama` 下 `updates / updates_v2 / *.log` 允许清理
  - 但本次在Trae沙盒内对该路径删除被策略拦截，未实际落盘删除
