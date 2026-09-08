---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_1a615a17693511f1a99c5254007bceed
    ReservedCode1: 9DlBOKO9mIGm7NuHBRyAWPHVKFg0JAuQD9cQUCFtqYfHCvjF68l/a8BYzCBC6acdyWFh+Y/i4fHkbkr+k2wUihR1SK+ki2e/IgKptc04IRAt9iAFU2tunaATrGlaz/Z6g4TDm/BkZn7VLkVT3EZrV8SD4x43lkLbkHWjfdNXdDxUDRDg0ZrmdbAKpZo=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_1a615a17693511f1a99c5254007bceed
    ReservedCode2: 9DlBOKO9mIGm7NuHBRyAWPHVKFg0JAuQD9cQUCFtqYfHCvjF68l/a8BYzCBC6acdyWFh+Y/i4fHkbkr+k2wUihR1SK+ki2e/IgKptc04IRAt9iAFU2tunaATrGlaz/Z6g4TDm/BkZn7VLkVT3EZrV8SD4x43lkLbkHWjfdNXdDxUDRDg0ZrmdbAKpZo=
---

# ZIP技能包打包规范

> 版本：v1.0 | 生效日期：2026-06-16 | 适用：CC Switch技能导入

---

## 一、核心原则

CC Switch「从ZIP安装」功能要求压缩包符合以下标准结构，否则将被拦截拒绝导入。

## 二、正确结构（合规）

压缩包内部第一层必须是**完整技能文件夹**：

```
pm-skills.zip
  └── pm-skills/              ← 外层总文件夹（必须）
        ├── skill.json        ← 技能主识别文件
        ├── SKILL.md          ← 技能详情文档
        ├── skills/           ← 子技能目录
        │     ├── 产品发现/
        │     ├── 产品战略/
        │     └── ...
        ├── slash-commands/   ← 快捷指令
        ├── plugins/          ← 插件模块
        ├── docs/             ← 文档
        └── pm-brain/         ← 产品知识库
```

**制作方法**：在技能根目录执行

```powershell
Compress-Archive -Path "pm-skills" -DestinationPath "pm-skills.zip"
```

或在文件资源管理器中，**右键技能文件夹 → 发送到 → 压缩(zipped)文件夹**。

## 三、错误结构（散包，将被拦截）

```
pm-skills.zip
  ├── skill.json              ← 没有外层总文件夹，文件零散平铺
  ├── SKILL.md
  ├── skills/
  ├── docs/
  └── ...                     ← 解压后污染全局技能库根目录
```

此结构将被CC Switch自动拒绝，并提示：「压缩包缺少外层技能文件夹，请重新按规范打包」。

## 四、校验规则

| 检查项 | 合规条件 | 不合规处理 |
|--------|---------|-----------|
| 根层级 | 第一层是单一文件夹 | 拒绝导入，弹窗提示 |
| 识别文件 | 文件夹根目录含 `skill.json` 或 `SKILL.md` | 拒绝导入，标注缺失 |
| 文件夹数量 | 第一层仅1个文件夹（技能包本体） | 多文件夹提示用户选择 |

## 五、注意事项

1. 不要直接选中文件夹内所有文件打包——必须选中文件夹本身再压缩
2. 不要将多个技能包打包在一个ZIP中
3. 压缩包文件名无限制，内部的技能文件夹名决定CC Switch面板显示
4. 备份包（如 `composio_backup_20260604`）同样遵循此规范
*（内容由AI生成，仅供参考）*
