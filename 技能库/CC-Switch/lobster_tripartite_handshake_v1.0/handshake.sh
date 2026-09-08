#!/usr/bin/env bash
set -euo pipefail

now_iso() {
  if command -v date >/dev/null 2>&1; then
    date -Iseconds
  else
    echo "unknown"
  fi
}

env_flag() {
  local name="$1"
  if [[ -n "${!name-}" ]]; then
    echo "SET"
  else
    echo "EMPTY"
  fi
}

tcp_check() {
  local host="$1"
  local port="$2"
  if [[ "$port" == "0" ]]; then
    echo "LOCAL"
    return 0
  fi
  if command -v timeout >/dev/null 2>&1; then
    timeout 1 bash -c "cat < /dev/null > /dev/tcp/${host}/${port}" >/dev/null 2>&1 && return 0 || return 1
  fi
  bash -c "cat < /dev/null > /dev/tcp/${host}/${port}" >/dev/null 2>&1 && return 0 || return 1
}

http_probe() {
  local base="$1"
  if [[ -z "$base" ]]; then
    echo "LOCAL"
    return 0
  fi
  if ! command -v curl >/dev/null 2>&1; then
    echo "NO_CURL"
    return 1
  fi
  local paths=("/healthz" "/health" "/v1/health" "/v1/models" "/")
  local p code
  for p in "${paths[@]}"; do
    code="$(curl -sS -o /dev/null -w "%{http_code}" --connect-timeout 1 --max-time 2 "${base%/}${p}" || true)"
    if [[ "$code" =~ ^[0-9]{3}$ ]] && [[ "$code" != "000" ]]; then
      echo "${code}:${p}"
      return 0
    fi
  done
  echo "NO_HTTP"
  return 1
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

STATE_DIR="${STATE_DIR-}"
if [[ -z "$STATE_DIR" ]]; then
  if [[ -n "${LOBSTER_STATE_DIR-}" ]]; then
    STATE_DIR="$LOBSTER_STATE_DIR"
  else
    STATE_DIR="/tmp/lobster_state/tripartite_handshake"
  fi
fi
mkdir -p "$STATE_DIR"

HERMES_HOST="${HERMES_HOST-127.0.0.1}"
HERMES_PORT="${HERMES_PORT-18080}"
DOUBAO_HOST="${DOUBAO_HOST-127.0.0.1}"
DOUBAO_PORT="${DOUBAO_PORT-18000}"
TRAE_HOST="${TRAE_HOST-127.0.0.1}"
TRAE_PORT="${TRAE_PORT-0}"

HERMES_BASE_URL="${HERMES_BASE_URL-}"
DOUBAO_BASE_URL="${DOUBAO_BASE_URL-}"
TRAE_BASE_URL="${TRAE_BASE_URL-}"

if [[ -z "$HERMES_BASE_URL" && "$HERMES_PORT" != "0" ]]; then HERMES_BASE_URL="http://${HERMES_HOST}:${HERMES_PORT}"; fi
if [[ -z "$DOUBAO_BASE_URL" && "$DOUBAO_PORT" != "0" ]]; then DOUBAO_BASE_URL="http://${DOUBAO_HOST}:${DOUBAO_PORT}"; fi
if [[ -z "$TRAE_BASE_URL" && "$TRAE_PORT" != "0" ]]; then TRAE_BASE_URL="http://${TRAE_HOST}:${TRAE_PORT}"; fi

ts="$(now_iso)"
skill="lobster_tripartite_handshake_v1.0"
version="v1.0"

index_path="${REPO_ROOT}/共享技能库/全局技能库/INDEX.jsonl"
local_skill_path="${REPO_ROOT}/.trae/skills/lobster_tripartite_handshake_v1.0/SKILL.md"

index_exists="false"; [[ -f "$index_path" ]] && index_exists="true"
local_skill_exists="false"; [[ -f "$local_skill_path" ]] && local_skill_exists="true"

skill_ids=("lobster_tripartite_handshake_v1.0" "lobster_self_learning_iteration_skill_v1.0" "lobster_claude_mem_gstack_bridge_v1.0")
skills_json=""
all_local_exist="true"
for sid in "${skill_ids[@]}"; do
  lp="${REPO_ROOT}/.trae/skills/${sid}/SKILL.md"
  le="false"; [[ -f "$lp" ]] && le="true"
  if [[ "$le" != "true" ]]; then all_local_exist="false"; fi
  se="false"
  if [[ -f "$index_path" ]] && grep -q "\"name\": \"${sid}\"" "$index_path" 2>/dev/null; then se="true"; fi
  if [[ -n "$skills_json" ]]; then skills_json+=", "; fi
  skills_json+="{\"id\":\"${sid}\",\"expected\":\"${version}\",\"local\":{\"path\":\"${lp}\",\"exists\":${le}},\"shared\":{\"fromIndex\":${se}}}"
done

requires_sync="false"
if [[ "$index_exists" != "true" || "$all_local_exist" != "true" || "$local_skill_exists" != "true" ]]; then
  requires_sync="true"
fi

nodes_json=""
online_count=0
offline_nodes=()

declare -A NAMES
NAMES[Hermes]="${HERMES_HOST}:${HERMES_PORT}:${HERMES_BASE_URL}"
NAMES[豆包]="${DOUBAO_HOST}:${DOUBAO_PORT}:${DOUBAO_BASE_URL}"
NAMES[Trae]="${TRAE_HOST}:${TRAE_PORT}:${TRAE_BASE_URL}"

for name in "Hermes" "豆包" "Trae"; do
  IFS=":" read -r host port base <<< "${NAMES[$name]}"
  physical_ok="false"
  if tcp_check "$host" "$port"; then physical_ok="true"; fi
  comm_ok="false"
  comm_info=""
  if [[ "$physical_ok" == "true" ]]; then
    if comm_info="$(http_probe "$base")"; then comm_ok="true"; else comm_ok="false"; fi
  fi
  online="false"
  if [[ "$physical_ok" == "true" && "$comm_ok" == "true" ]]; then
    online="true"
    online_count=$((online_count+1))
  else
    offline_nodes+=("$name")
  fi
  if [[ -n "$nodes_json" ]]; then nodes_json+=", "; fi
  nodes_json+="{\"name\":\"${name}\",\"host\":\"${host}\",\"port\":${port},\"baseUrl\":\"${base}\",\"physicalOk\":${physical_ok},\"commOk\":${comm_ok},\"commInfo\":\"${comm_info}\",\"online\":${online}}"
done

overall="OK"
if [[ "$online_count" -lt 2 ]]; then overall="DEGRADED"; fi
if [[ "$online_count" -eq 0 ]]; then overall="OFFLINE"; fi
if [[ "$requires_sync" == "true" && "$overall" == "OK" ]]; then overall="DEGRADED"; fi

report_path="${STATE_DIR}/tripartite_handshake_last_report.json"
link_path="${STATE_DIR}/tripartite_handshake_link.json"
pending_path="${STATE_DIR}/tripartite_pending_sync.json"

report_json="{\"skill\":\"${skill}\",\"version\":\"${version}\",\"ts\":\"${ts}\",\"repoRoot\":\"${REPO_ROOT}\",\"overall\":\"${overall}\",\"requiresSync\":${requires_sync},\"nodes\":[${nodes_json}],\"app\":{\"index\":{\"path\":\"${index_path}\",\"exists\":${index_exists}},\"skills\":[${skills_json}],\"tokens\":{\"LOBSTER_MASTER_TOKEN\":\"$(env_flag LOBSTER_MASTER_TOKEN)\",\"HERMES_API_TOKEN\":\"$(env_flag HERMES_API_TOKEN)\",\"HERMES_LOCAL_KEY\":\"$(env_flag HERMES_LOCAL_KEY)\",\"TRAE_TOKEN\":\"$(env_flag TRAE_TOKEN)\"}}}"

printf "%s\n" "$report_json" > "$report_path"
printf "%s\n" "$report_json"

if [[ "$online_count" -ge 2 ]]; then
  printf "%s\n" "$report_json" > "$link_path"
fi

if [[ "$requires_sync" == "true" ]]; then
  printf "%s\n" "{\"ts\":\"${ts}\",\"reason\":\"VERSION_OR_INDEX_OR_DOC_MISMATCH\",\"expectedVersion\":\"${version}\",\"indexExists\":${index_exists},\"allLocalExist\":${all_local_exist},\"localHandshakeSkillExists\":${local_skill_exists}}" > "$pending_path"
fi

if [[ "$overall" == "OFFLINE" ]]; then exit 2; fi
if [[ "$requires_sync" == "true" ]]; then exit 3; fi
if [[ "$overall" == "DEGRADED" ]]; then exit 1; fi
exit 0
