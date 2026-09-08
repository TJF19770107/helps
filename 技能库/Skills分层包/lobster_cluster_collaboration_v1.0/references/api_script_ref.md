# API Script Reference

> Layer3 引用文档 — 龙虾协作脚本规范

## 脚本模板 (lobster_script_template.py)

```python
#!/usr/bin/env python3
"""
龙虾协作脚本模板 v1.0
用法: python lobster_script_template.py --task-id TASK_ID --mode MODE
"""
import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# === 配置区 ===
CLUSTER_ROOT = Path(r"E:\龙虾AI主控中心\我的AI分身\技能库\协作脚本")
COLLAB_ARCHIVE = Path(r"E:\龙虾AI主控中心\我的AI分身\技能库\协作档案")

# === 工具函数 ===
def log_event(event_type: str, payload: dict):
    """写入协作事件日志"""
    log_line = json.dumps({
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        **payload
    }, ensure_ascii=False)
    print(log_line, flush=True)

def handoff_artifact(source_agent: str, target_agent: str, artifact_path: str):
    """流水线产物传递"""
    # 复制到目标Agent工作目录
    pass

def check_consensus(results: list[dict]) -> dict:
    """共识校验：比较多个Agent的独立推理结果"""
    if not results:
        return {"consensus": False, "reason": "no_results"}
    # 简单多数一致判定
    return {"consensus": True, "confidence": 0.9, "agreement_count": len(results)}

# === 主函数 ===
def main():
    parser = argparse.ArgumentParser(description="龙虾协作脚本")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--mode", required=True,
                        choices=["INFO_PASS", "TASK_DELEGATE", "PARALLEL_DIVIDE",
                                 "PIPELINE_HANDOFF", "CONSENSUS_CHECK",
                                 "MUTUAL_MCP", "CLUSTER_DEBATE"])
    parser.add_argument("--payload", default="{}")
    args = parser.parse_args()

    payload = json.loads(args.payload)
    log_event("SCRIPT_START", {"task_id": args.task_id, "mode": args.mode})
    # === 模式分发 ===
    if args.mode == "INFO_PASS":
        result = {"status": "broadcasted", "recipients": payload.get("agents", [])}
    elif args.mode == "CONSENSUS_CHECK":
        result = check_consensus(payload.get("results", []))
    else:
        result = {"status": "executed", "mode": args.mode}
    log_event("SCRIPT_END", {"task_id": args.task_id, "result": result})
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

## PowerShell 协作脚本模板

```powershell
<#
.SYNOPSIS
  龙虾协作 PowerShell 脚本模板 v1.0
.DESCRIPTION
  在Windows环境下执行协作任务的标准化脚本
.PARAMETER TaskId
  任务唯一标识
.PARAMETER Mode
  协作模式：INFO_PASS|TASK_DELEGATE|PARALLEL_DIVIDE|...
.PARAMETER PayloadJson
  任务负载JSON字符串
#>
param(
    [Parameter(Mandatory=$true)] [string]$TaskId,
    [Parameter(Mandatory=$true)] [ValidateSet("INFO_PASS","TASK_DELEGATE","PARALLEL_DIVIDE","PIPELINE_HANDOFF","CONSENSUS_CHECK","MUTUAL_MCP","CLUSTER_DEBATE")] [string]$Mode,
    [string]$PayloadJson = "{}"
)

$ScriptRoot = "E:\龙虾AI主控中心\我的AI分身\技能库\协作脚本"
$ArchiveRoot = "E:\龙虾AI主控中心\我的AI分身\技能库\协作档案"

function Write-CollabLog {
    param([string]$EventType, [hashtable]$Payload)
    $log = @{ timestamp = (Get-Date -Format "o"); event_type = $EventType } + $Payload
    $log | ConvertTo-Json -Compress | Write-Output
}

Write-CollabLog "SCRIPT_START" @{ task_id = $TaskId; mode = $Mode }
# ... 模式分发逻辑 ...
Write-CollabLog "SCRIPT_END" @{ task_id = $TaskId; status = "completed" }
```

## 脚本命名规范

```
lobster_{mode}_{function}_v{major}.{minor}.{ext}

示例:
  lobster_info_broadcast_v1.0.py
  lobster_consensus_check_v1.0.ps1
  lobster_pipeline_handoff_v1.0.py
  lobster_cluster_debate_v1.0.ps1
```
