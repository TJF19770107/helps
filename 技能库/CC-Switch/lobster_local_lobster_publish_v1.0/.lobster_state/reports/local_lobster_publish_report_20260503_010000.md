【Trae发布验收】2026-05-03 | 本地龙虾闭环发布（方案A：纯本地固化标准版）

## 1) 固化目标（不涉及云端）

- 固定本地接口（不再改动）：http://127.0.0.1:18091/api/trae/skills/list
- 固定验收口径：必须满足 `ok:true` 且 `skills` 为数组

## 2) 已发布为独立全局技能

- Trae 右侧全局技能目录（可见）：  
  - E:\龙虾AI主控中心\.trae\skills\lobster_local_lobster_publish_v1.0
- 本机共享技能根目录（可被本地智能体加载）：  
  - C:\Users\Administrator\.claude\skills\_trae_skills\lobster_local_lobster_publish_v1.0
- Hermes 注入目录（已同步生成）：  
  - E:\龙虾AI主控中心\.hermes\skills\lobster_local_lobster_publish_v1.0

## 3) 技能能力（对外函数）

- skill_local_lobster_skills_health：调用 /api/trae/skills/health 并落盘取证
- skill_local_lobster_skills_list：调用 /api/trae/skills/list 并校验 skills 数组，落盘取证
- skill_local_lobster_publish_acceptance：一键跑 health + list，输出验收摘要并落盘

## 4) 取证与验收（2xx + 结构校验）

- 一键验收审计（JSON）：  
  - E:\龙虾AI主控中心\.trae\skills\lobster_local_lobster_publish_v1.0\.lobster_state\reports\local_lobster_acceptance_20260503_005842.json
- health 取证（JSON）：  
  - E:\龙虾AI主控中心\.trae\skills\lobster_local_lobster_publish_v1.0\.lobster_state\reports\local_lobster_skills_health_20260503_005842.json
- list 取证（JSON，含 ok:true + skills 数组校验）：  
  - E:\龙虾AI主控中心\.trae\skills\lobster_local_lobster_publish_v1.0\.lobster_state\reports\local_lobster_skills_list_20260503_005842.json

## 5) 安全口径（不泄露机密）

- Bearer Token 仅从环境变量读取（TRAE_API_TOKEN 或 DOUBAO_USER_TRIGGER_TOKEN）
- 审计仅记录 authorization_present 与 token_env（变量名），不记录任何 Token 明文

## 6) 最小复跑命令（可复现）

```powershell
python -c "import sys,json; sys.path.insert(0, r'E:\龙虾AI主控中心\.trae\skills\lobster_local_lobster_publish_v1.0'); import skill_entry as s; print(json.dumps(s.skill_local_lobster_publish_acceptance(), ensure_ascii=False))"
```

