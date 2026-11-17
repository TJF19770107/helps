# -*- coding: utf-8 -*-
"""
prepare_write_payload.py —— 准备「网页 → 得到大脑」写入体（写 Obsidian 待回写目录 + 打印 payload）

产出：
  1. Obsidian 主库：02_产物归档/待回写得到大脑/20261117_产品灵感_得到大脑.md（正式条目，含四化拆解）
  2. payload JSON：写入器直接消费（title / content / url / tags）
"""
import os, sys, json, urllib.parse, hashlib

sys.stdout.reconfigure(encoding="utf-8")

from obsidian_rest import ObsidianRest

URL = "https://www.biji.com"
TITLE = "得到大脑 - 用AI重新定义个人记录与创作"
TAG = "产品灵感"

BODY = """**来源链接**：https://www.biji.com
**采集时间**：2026-11-17 10:53:49
**网页标题**：得到大脑 - 用AI重新定义个人记录与创作
**渠道**：网页版可达性探测 / 本轮 OAuth Device Flow 打通写入通道

---

## 一、产品是什么

得到大脑（Get笔记）= 订阅制个人记录与创作工具：
- **订阅博主**：每天早 8 点自动更新前一天发布的新视频/文章（增量，不是历史全量）
- **多模态采集**：抖音 / 小红书 / B站 / 公众号 / 微信聊天 → 转文字 + 存原文
- **知识沉淀**：笔记 → 知识库（topic）→ 目录 → 标签体系
- **变现钩子**：付费订阅 299/年（OpenAPI 会员墙）

## 二、痛点（用户真正的阻力）

| 阻力 | 表现 | 我们的解法 |
|---|---|---|
| 内容散落 | 刷到的有价值内容存不住、找不到 | 订阅博主 → 自动入库 |
| 摘抄成本高 | 手抄一遍才开始思考 | 语音/视频自动转文字 → 直接沉淀 |
| 素材不产粮 | 收藏了但用不上 | 四化拆解 → 可对标脚本/模板/技能 |
| 平台墙 | 抖音不能批量导出 | 本机 ffmpeg + faster-whisper 零付费转写 |

## 三、最小可行（1 天内能收费的最小版本）

**「抖音爆款 → 可对标口播脚本」订阅包**
- 输入：汤哥指定的 3-5 个对标博主
- 流程：抖音视频 → 本机下载 → ffmpeg 抽音轨 → faster-whisper 转写 → 四化拆解（钩子/结构/情绪/落点）→ 输出对标脚本表
- 交付：每周 5 条对标脚本 + 1 份拆解报告（Markdown/PDF）
- 定价锚点：单条 30-50 元，月度包 199-299 元（对标零积分排版接单口径）

## 四、变现路径（三条，选一条主攻）

1. **接单**：给做 IP 的个人/小团队卖「对标博主内容拆解」——最快现金流
2. **自有产品**：把四化拆解框架做成 Skill/模板包，在知识库/IMA/乐享挂付费咨询
3. **知识库付费**：把拆解后的方法论沉淀成体系文档，做会员社群

## 五、沉淀（转技能/模板）

- 技能：`得到大脑Obsidian四化拆解` v2.0.0（已落地，16448 B）
- 脚本：`obsidian_rest.py`（REST 客户端库）、`dedao_bridge.py`（三通道桥）、
  `media_transcribe.py`（语音转写）、`dedao_web_writer.py`（网页写入器）、
  `oauth_device_run.py`（Device Flow 授权）
- 通道：Obsidian REST ✅ 8/8 L4 · 得到大脑网页后端 ✅ 本轮打通

## 六、待办

- [ ] 汤哥手机订阅 ≥1 个抖音博主（图文增量通道，与语音通道是两回事）
- [ ] 用真实博主跑一遍「转写 → 拆解 → 脚本」端到端，出 1 份可报价的样例
- [ ] CNB 知识库专用仓建好后补齐六端归档
"""

r = ObsidianRest()
rel = "02_产物归档/待回写得到大脑/20261117_产品灵感_得到大脑.md"
st, msg = r.write(rel, BODY)
print(f"写入 Obsidian: {st} {msg}")

st2, raw = r.call("/vault/" + urllib.parse.quote(rel),
                  headers={"Accept": "application/vnd.olrapi.document-content+json"})
sha_disk = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
sha_src = hashlib.sha256(BODY.encode("utf-8")).hexdigest()[:16]
print(f"回读 sha 磁盘={sha_disk}  源={sha_src}  一致={sha_disk == sha_src}")

payload = {
    "title": TITLE,
    "content": BODY,
    "url": URL,
    "tags": [TAG],
}
pf = r"E:\博主学习库\_tools\write_payload.json"
with open(pf, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
print(f"\npayload 已存: {pf}")
print(json.dumps(payload, ensure_ascii=False)[:400])
