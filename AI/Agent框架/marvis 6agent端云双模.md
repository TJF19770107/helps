# Marvis 6-Agent 端云双模架构

> **来源**: CSDN + 腾讯云 + 腾讯网 + 网易, 2026-05
> **豆包关联**: R02深度迭代报告 · 本土对标
> **MOC**: [[_MOC_AI Agent框架]]

---

## 6-Agent协作体系

```
PM Agent (主调度) → 意图理解 + 任务拆解 + 结果汇总
  ├── File Agent: 文件搜索/格式转换/OCR
  ├── Computer Agent: 系统设置/故障排查/桌面控制(Windows API直调)
  ├── App Agent: 应用安装/卸载/GUI视觉识别+模拟操作
  ├── Browser Agent: 网页交互/登录/表单/DOM解析
  └── Search Agent: 深度搜索/信息聚合
```

## 端云双模自动路由

| 模式 | 模型 | 场景 |
|------|------|------|
| 效率模式 | 混元 + DeepSeek V4 云端推理 | 复杂任务、深度分析 |
| 隐私模式 | Qwen + Intel OpenVINO 端侧推理 | 敏感数据、离线场景 |

## OS级AI中间层

```
用户 → 自然语言 → Agent → OS API → 文件/设置/应用/硬件
```

## 豆包在Marvis平台上的增量价值定位

| Marvis提供 | 豆包提供 |
|-----------|---------|
| 6-Agent调度体系 | 自进化闭环（持续学习优化） |
| 端云双模自动路由 | Obsidian知识库深度联动 |
| 多端协同 | 全域能力对标迭代 |
| 端侧加密 | 2h+3h双循环自动化 |
| OS级AI中间层 | PARA+MOC+运维手册知识管理 |

---

**标签**: #AI/Agent框架 #Marvis #端云双模 #6Agent #OS级AI