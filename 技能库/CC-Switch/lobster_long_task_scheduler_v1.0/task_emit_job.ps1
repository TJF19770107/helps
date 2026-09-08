param(
  [Parameter(Mandatory = $true)]
  [string]$JobName
)

$ErrorActionPreference = "Stop"

function Resolve-SkillDir() {
  return (Resolve-Path $PSScriptRoot).Path
}

$skillDir = Resolve-SkillDir

$py = @"
import json
import os
import sys
from pathlib import Path

skill_dir = Path(r"$skillDir")
sys.path.insert(0, str(skill_dir))

from main import emit_job

res = emit_job(r"$JobName", skill_dir=skill_dir)
print(json.dumps(res, ensure_ascii=False))
"@

python -c $py

