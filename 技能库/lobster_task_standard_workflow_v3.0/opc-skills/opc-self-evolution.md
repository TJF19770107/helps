---
name: opc-self-evolution
description: 自我进化：为 OPC 每个阶段产出生成测试提示、版本记录与反馈回路，支持技能持续迭代。
triggers:
  - 自我进化
  - 迭代技能
  - test prompts
  - 反馈回路
---

# OPC 自我进化技能

## 进化流程
1. 读取当前阶段产出 Markdown。
2. 生成 3-5 个测试提示（覆盖正常 / 边界 / 异常场景）。
3. 把测试提示写入 `opc-doc/outputs/{阶段}/test-prompts.json`。
4. 记录版本、变更原因、待验证假设到 `opc-doc/outputs/{阶段}/CHANGELOG.md`。
5. 根据运行反馈回炉迭代。

## 测试提示模板
```json
{
  "id": "opc-{stage}-{n}",
  "scenario": "正常/边界/异常",
  "input": "用户输入示例",
  "expected": "预期输出或动作",
  "validation": "如何判断通过"
}
```

## 反馈回路
- 每次运行后追加 `run-log.md`。
- 连续 3 次失败触发技能修正。
- 成功用例沉淀为最佳实践。
