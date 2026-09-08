---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_5b112dd190ea11f1a102525400826444
    ReservedCode1: VjfgaISYq4vA4qDLb2fSaij/s1XkMLl5avXWhNUn0mRdpS/7Hc13uUgWFbPYeeEfakxiKHNQYcM5799j9SQzoqBFXUy5AgOPEQdCpC4MDyE/SEepk6iUjemSP9bQuhUvoHQO2EtfjI0O1RWtoZkf+hidPuvkVPxmCgI3A/SBc/1W6ro1ENRK/Z4fp+g=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_5b112dd190ea11f1a102525400826444
    ReservedCode2: VjfgaISYq4vA4qDLb2fSaij/s1XkMLl5avXWhNUn0mRdpS/7Hc13uUgWFbPYeeEfakxiKHNQYcM5799j9SQzoqBFXUy5AgOPEQdCpC4MDyE/SEepk6iUjemSP9bQuhUvoHQO2EtfjI0O1RWtoZkf+hidPuvkVPxmCgI3A/SBc/1W6ro1ENRK/Z4fp+g=
---



# 龙虾学习模板 v1.0

> 版本：v1.0 | 创建：2026-08-05 | 所属：赛博书屋 v1.5 子模块
> 定位：触发词驱动的全链路学习自动化模板
> 依赖：赛博书屋（抓取） → 仓颉蒸馏（萃取） → Obsidian（沉淀）

---

## 触发词

| 触发词 | 示例 |
|--------|------|
| `学习` | "学习天锋教你玩Ai" |
| `学这个博主` | "学这个博主的所有内容" |
| `研究` | "研究XXX的创作方法论" |
| `萃取这个` | "萃取这个号的精华" |
| `学习这个号` | "学习这个号的全部视频" |

---

## 五步全链路流程

### ① 赛博书屋抓取目标内容

当用户说出触发词后，自动识别博主/账号名，通过赛博书屋执行全平台抓取：

| 平台 | 抓取内容 | 工具 |
|------|----------|------|
| 视频号 | 标题/描述/发布者/话题标签 | web_fetch |
| 公众号 | 文章正文/作者/发布时间 | web_fetch + 浏览器插件 |
| B站 | 字幕/简介/评论区/UP主信息 | 浏览器 + OCR |
| YouTube | 字幕/描述/频道信息 | 浏览器 + yt-dlp |
| X/Twitter | 推文文本/发布者/引用链接 | web_fetch |

### ② 结构化笔记写入 Obsidian

抓取结果按标准模板写入 `E:\龙虾AI主控中心\Obsidian\wiki\赛博书屋\`：

```markdown
---
来源: {平台}
作者: {博主}
发布日期: {日期}
原始链接: {URL}
标签: {自动提取标签}
---

# {标题}

## 核心内容
{摘要/描述}

## 关键信息
{结构化提取}

## 关联
[[赛博书屋]] [[仓颉Skill]] [[龙虾五步法V3.0]]
```

### ③ 仓颉蒸馏桥接自动触发

赛博书屋新笔记写入后，`cangjie_bridge.py` 自动扫描并触发蒸馏：

```
新笔记 → cangjie_bridge.py 检测
  → 格式化为 RIA-TV++ 输入
  → 调用仓颉Skill RIA-TV++ 蒸馏流水线
  → 提取可复用技能单元
```

### ④ 产出注册到龙虾五步法技能生态

蒸馏产出的技能单元自动注册：
- 技能 .md 文件 → `E:\龙虾AI主控中心\我的AI分身\技能库\`
- 知识文档 → `E:\龙虾AI主控中心\Obsidian\wiki\`
- 软链接注册 → 龙虾五步法「十一、技能生态系统」

### ⑤ 通知用户完成

全链路执行完毕，输出摘要：
- 抓取了 X 条内容
- 蒸馏出 Y 个技能单元
- 全部已沉淀到 Obsidian

---

## 示例用法

### 示例 1：学习视频号博主

```
用户：学习天锋教你玩Ai

执行流程：
  ① 赛博书屋抓取"天锋教你玩Ai"全部公开视频号内容
  ② 每条视频生成结构化 Obsidian 笔记
  ③ 仓颉蒸馏桥接自动触发 → 提取 AI 智能体 / Codex 工作流 等技能单元
  ④ 产出注册到龙虾五步法技能生态
  ⑤ 通知：已抓取 N 个视频，蒸馏出 M 个技能单元，全部已入库
```

### 示例 2：学习 B站 UP主

```
用户：研究 xxx 的创作方法论

执行流程：
  ① 赛博书屋抓取 xxx B站全部视频（字幕 + 简介 + 评论）
  ② 结构化笔记写入 Obsidian
  ③ 仓颉蒸馏提取创作方法论技能单元
  ④ 注册到龙虾五步法技能生态
```

### 示例 3：学习公众号

```
用户：萃取这个号的精华

执行流程：
  ① 赛博书屋抓取该公众号历史文章
  ② 笔记分级：精华 / 一般 / 参考
  ③ 仓颉蒸馏对精华内容深度萃取
  ④ 产出知识技能包
```

---

## 配置项

| 配置 | 默认值 | 说明 |
|------|--------|------|
| `OBSIDIAN_CYBER_DIR` | `E:\龙虾AI主控中心\Obsidian\wiki\赛博书屋\` | 笔记写入目录 |
| `CANGJIE_BRIDGE` | `cyber-book-house/cangjie_bridge.py` | 蒸馏桥接脚本 |
| `AUTO_DISTILL` | true | 是否自动触发蒸馏 |
| `MAX_ITEMS_PER_SOURCE` | 50 | 单次抓取上限 |

---

**模板生成**：Hermes Agent | 龙虾学习模板 v1.0
**版本控制**：v1.0 | 2026-08-05
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
