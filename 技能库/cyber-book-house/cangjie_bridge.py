#!/usr/bin/env python3
"""cangjie_bridge.py — 赛博书屋 → 仓颉蒸馏 桥接器

功能：
  - 扫描赛博书屋 Obsidian 产出目录
  - 对新文件自动触发仓颉蒸馏流程
  - 将笔记格式化为仓颉 RIA-TV++ 所需输入格式
  - 调用仓颉蒸馏模板生成技能单元
"""

import os
import re
import json
import hashlib
from datetime import datetime

# ===================== 路径配置 =====================

OBSIDIAN_CYBER_DIR = r"E:\龙虾AI主控中心\Obsidian\wiki\赛博书屋"
CANGJIE_SKILL_DIR = r"E:\龙虾AI主控中心\我的AI分身\技能库\cangjie-skill"
BRIDGE_RECORD_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "cangjie_bridge_record.json"
)


# ===================== 扫描函数 =====================

def scan_new_notes(obsidian_dir: str = None) -> list:
    """扫描赛博书屋目录，列出未蒸馏的新笔记。

    Args:
        obsidian_dir: Obsidian赛博书屋目录，默认使用全局配置

    Returns:
        list: 未蒸馏笔记的绝对路径列表
    """
    if obsidian_dir is None:
        obsidian_dir = OBSIDIAN_CYBER_DIR

    if not os.path.exists(obsidian_dir):
        print(f"[cangjie_bridge] 目录不存在: {obsidian_dir}")
        return []

    # 加载蒸馏记录
    distilled = _load_record()

    new_notes = []
    for root, dirs, files in os.walk(obsidian_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            fhash = _file_hash(fpath)
            if fhash not in distilled:
                new_notes.append(fpath)

    return new_notes


# ===================== 格式化 =====================

def prepare_for_distill(note_path: str) -> dict:
    """将 Obsidian 笔记格式化为仓颉 RIA-TV++ 所需输入格式。

    Args:
        note_path: 笔记文件路径

    Returns:
        dict: RIA-TV++ 格式的结构化数据
    """
    with open(note_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析 Front Matter
    front_matter = {}
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                front_matter[key.strip()] = val.strip()

    # 提取正文（去掉 Front Matter）
    body = content
    if fm_match:
        body = content[fm_match.end():].strip()

    # 构造 RIA-TV++ 输入
    ria_input = {
        "meta": {
            "source": front_matter.get("来源", "未知"),
            "author": front_matter.get("作者", "未知"),
            "publish_date": front_matter.get("发布日期", ""),
            "original_url": front_matter.get("原始链接", ""),
            "tags": front_matter.get("标签", ""),
            "note_path": note_path,
            "file_hash": _file_hash(note_path),
        },
        "body": body,
        "word_count": len(body),
    }

    return ria_input


# ===================== 蒸馏流水线 =====================

def run_distill_pipeline(note_path: str) -> dict:
    """调用仓颉蒸馏模板，对笔记内容执行 RIA-TV++ 蒸馏。

    Args:
        note_path: 笔记文件路径

    Returns:
        dict: 蒸馏结果状态
    """
    if not os.path.exists(note_path):
        return {"status": "error", "message": f"文件不存在: {note_path}"}

    # Step 1: 格式化为 RIA-TV++ 输入
    ria_data = prepare_for_distill(note_path)

    # Step 2: 生成蒸馏摘要文件（桥接到仓颉Skill处理目录）
    distill_input_dir = os.path.join(CANGJIE_SKILL_DIR, "input")
    os.makedirs(distill_input_dir, exist_ok=True)

    distill_input_path = os.path.join(
        distill_input_dir,
        f"distill_{ria_data['meta']['file_hash']}.json"
    )

    with open(distill_input_path, "w", encoding="utf-8") as f:
        json.dump(ria_data, f, ensure_ascii=False, indent=2)

    # Step 3（v1.1补完）：生成仓颉蒸馏 Agent 指令
    # 之前的版本到这里就断了，JSON 放进 input/ 但没有指令让 Agent 去跑提取器。
    # 现在补上：生成指令文件，Agent（Marvis/Hermes）读取后按仓颉SKILL.md执行蒸馏。
    agent_instruction = _generate_distill_instruction(ria_data, distill_input_path)

    # Step 4: 标记为已蒸馏
    _mark_distilled(note_path)

    return {
        "status": "ok",
        "note_path": note_path,
        "distill_input": distill_input_path,
        "agent_instruction": agent_instruction,
        "word_count": ria_data["word_count"],
        "message": "RIA-TV++ 输入已生成，Agent 指令已写入。请 Agent 读取指令执行仓颉蒸馏。",
    }


# ===================== 辅助函数 =====================

def _generate_distill_instruction(ria_data: dict, distill_input_path: str) -> str:
    """v1.1补完：生成仓颉蒸馏 Agent 指令文件

    之前的版本只把 JSON 放到 input/ 就结束了，没有指令让 Agent 去跑提取器。
    现在生成一个指令文件，Agent 读取后按仓颉SKILL.md执行五阶段蒸馏。

    Args:
        ria_data: RIA-TV++ 格式的结构化数据
        distill_input_path: 蒸馏输入JSON路径

    Returns:
        str: 指令文件路径
    """
    instruction_dir = os.path.join(CANGJIE_SKILL_DIR, "input")
    os.makedirs(instruction_dir, exist_ok=True)

    instruction_path = os.path.join(
        instruction_dir,
        f"INSTRUCTION_{ria_data['meta']['file_hash']}.md"
    )

    meta = ria_data.get("meta", {})
    word_count = ria_data.get("word_count", 0)

    instruction_content = f"""# 仓颉蒸馏 Agent 指令

> 自动生成 | cangjie_bridge.py v1.1 | {datetime.now().isoformat()}

## 蒸馏目标
- **来源**: {meta.get('source', '未知')}
- **作者**: {meta.get('author', '未知')}
- **原始链接**: {meta.get('original_url', '')}
- **字数**: {word_count}
- **输入文件**: `{distill_input_path}`

## 执行步骤（按仓颉SKILL.md RIA-TV++ 流水线）

### 阶段0: Adler整书理解
读取 `{distill_input_path}` 中的 body 字段，生成 BOOK_OVERVIEW.md

### 阶段1: 并行提取（5个提取器）
调用仓颉 extractors/ 目录下的5个提取器prompt：
1. `framework-extractor.md` → 决策框架/思维模型
2. `principle-extractor.md` → 原则/清单/规则
3. `case-extractor.md` → 作者亲自使用过的实例
4. `counter-example-extractor.md` → 警告的失败模式
5. `glossary-extractor.md` → 关键概念词典

### 阶段1.5: 三重验证
- V1跨域: 原文中至少2处独立段落佐证
- V2预测力: 能回答原文未明说的新问题
- V3独特性: 不是常识性内容

### 阶段2: RIA++ 构造
将通过验证的单元构造为 SKILL.md（R/I/A1/A2/E/B 六段）

### 阶段3: Zettelkasten链接
生成 INDEX.md + GLOSSARY.md

### 阶段4: 压力测试
生成 test-prompts.json，不合格单元回炉

### 阶段5: 交付
生成 DIGEST.md，安装到 skills 目录

## 输出位置
```
cangjie-skill/output/{meta.get('file_hash', 'unknown')}/
├── BOOK_OVERVIEW.md
├── SKILL.md
├── INDEX.md
├── GLOSSARY.md
├── DIGEST.md
└── test-prompts.json
```
"""

    with open(instruction_path, "w", encoding="utf-8") as f:
        f.write(instruction_content)

    return instruction_path


def _file_hash(filepath: str) -> str:
    """计算文件内容 MD5 哈希"""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def _load_record() -> set:
    """加载已蒸馏记录"""
    if os.path.exists(BRIDGE_RECORD_FILE):
        with open(BRIDGE_RECORD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("distilled_hashes", []))
    return set()


def _mark_distilled(filepath: str):
    """将文件标记为已蒸馏"""
    records = {}
    if os.path.exists(BRIDGE_RECORD_FILE):
        with open(BRIDGE_RECORD_FILE, "r", encoding="utf-8") as f:
            records = json.load(f)

    fhash = _file_hash(filepath)
    if "distilled_hashes" not in records:
        records["distilled_hashes"] = []

    if fhash not in records["distilled_hashes"]:
        records["distilled_hashes"].append(fhash)
        records["last_updated"] = datetime.now().isoformat()

    with open(BRIDGE_RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


# ===================== CLI入口 =====================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("cangjie_bridge.py — 赛博书屋 → 仓颉蒸馏 桥接器")
        print("用法:")
        print("  python cangjie_bridge.py --scan           扫描未蒸馏笔记")
        print("  python cangjie_bridge.py --distill-all    蒸馏所有新笔记")
        print("  python cangjie_bridge.py --distill <path> 蒸馏指定笔记")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "--scan":
        notes = scan_new_notes()
        print(f"发现 {len(notes)} 个未蒸馏笔记:")
        for n in notes:
            print(f"  - {n}")

    elif cmd == "--distill-all":
        notes = scan_new_notes()
        if not notes:
            print("没有未蒸馏的笔记。")
            sys.exit(0)

        for note_path in notes:
            result = run_distill_pipeline(note_path)
            print(f"[{'OK' if result['status']=='ok' else 'FAIL'}] {note_path}")

    elif cmd == "--distill":
        if len(sys.argv) < 3:
            print("请指定笔记路径: python cangjie_bridge.py --distill <path>")
            sys.exit(1)
        note_path = sys.argv[2]
        result = run_distill_pipeline(note_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
