#!/bin/bash
# ============================================================
# Agent-Reach Linux/macOS 安装脚本
# 自动检测环境、安装依赖、配置代理
# 版本: 1.0.0 | 日期: 2026-06-14
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_DIR="${SCRIPT_DIR}/logs"
DOCTOR_LOG="${SCRIPT_DIR}/doctor-log.txt"
INSTALL_LOG="${LOG_DIR}/install-$(date +%Y%m%d).log"

mkdir -p "$LOG_DIR"

# 日志函数
log() {
    local level="${2:-INFO}"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local entry="[${timestamp}] [${level}] $1"
    echo "$entry"
    echo "$entry" >> "$INSTALL_LOG"
}

log "=== Agent-Reach 安装脚本启动 ==="
log "项目根目录: ${PROJECT_ROOT}"

# ============================================================
# 步骤1: 检查 Python 3.10+ 环境
# ============================================================
log "步骤1: 检查 Python 环境..."

PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    log "未找到 Python，请先安装 Python 3.10+" "ERROR"
    echo "错误: 未找到 Python，请安装 Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
log "Python 版本: ${PYTHON_VERSION}"

PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]; }; then
    log "Python 版本不满足要求（需要 3.10+），当前: ${PYTHON_VERSION}" "ERROR"
    exit 1
fi
log "Python 版本检查通过"

# ============================================================
# 步骤2: 升级 pip 并安装 agent-reach
# ============================================================
log "步骤2: 安装 agent-reach..."

$PYTHON_CMD -m pip install --upgrade pip 2>&1 | while read line; do log "pip upgrade: $line"; done

if ! $PYTHON_CMD -m pip install agent-reach 2>&1 | while read line; do log "pip install: $line"; done; then
    log "agent-reach 安装失败，尝试从 GitHub 直接安装..." "WARN"
    if ! $PYTHON_CMD -m pip install https://github.com/Panniantong/agent-reach/archive/main.zip 2>&1 | while read line; do log "pip github: $line"; done; then
        log "agent-reach 安装失败" "ERROR"
        exit 1
    fi
fi
log "agent-reach 安装完成"

# ============================================================
# 步骤3: 执行 agent-reach doctor 并保存日志
# ============================================================
log "步骤3: 执行 agent-reach doctor..."

if $PYTHON_CMD -m agent_reach doctor 2>&1 | tee "$DOCTOR_LOG"; then
    log "doctor 日志已保存至: ${DOCTOR_LOG}"
else
    log "尝试备用方式: agent-reach doctor" "WARN"
    agent-reach doctor 2>&1 | tee "$DOCTOR_LOG" || log "agent-reach doctor 失败" "WARN"
fi

# ============================================================
# 步骤4: 执行 agent-reach install --env=auto
# ============================================================
log "步骤4: 执行 agent-reach install --env=auto..."

if $PYTHON_CMD -m agent_reach install --env=auto 2>&1 | while read line; do log "install: $line"; done; then
    :
else
    agent-reach install --env=auto 2>&1 | while read line; do log "install: $line"; done || {
        log "agent-reach install 失败" "ERROR"
        exit 1
    }
fi
log "agent-reach install 完成"

# ============================================================
# 步骤5: 配置代理
# ============================================================
log "步骤5: 配置代理..."

PROXY_URL="http://127.0.0.1:6738"

if $PYTHON_CMD -m agent_reach config set proxy.http "$PROXY_URL" 2>&1 | while read line; do log "proxy config: $line"; done; then
    $PYTHON_CMD -m agent_reach config set proxy.https "$PROXY_URL" 2>&1 | while read line; do log "proxy config: $line"; done
else
    agent-reach config set proxy.http "$PROXY_URL" 2>&1 | while read line; do log "proxy config: $line"; done || log "代理配置失败，请手动执行" "WARN"
    agent-reach config set proxy.https "$PROXY_URL" 2>&1 | while read line; do log "proxy config: $line"; done
fi

# ============================================================
# 步骤6: 验证安装
# ============================================================
log "步骤6: 验证安装..."

if version=$($PYTHON_CMD -m agent_reach --version 2>&1); then
    log "agent-reach 版本: ${version}"
else
    agent-reach --version 2>&1 | while read line; do log "version: $line"; done || log "无法获取版本号，但安装流程已完成" "WARN"
fi

# ============================================================
# 完成
# ============================================================
log "=== Agent-Reach 安装脚本完成 ==="
echo ""
echo "========================================"
echo "  Agent-Reach 安装完成！"
echo "========================================"
echo "  Doctor 日志: ${DOCTOR_LOG}"
echo "  安装日志: ${LOG_DIR}"
echo "  下一步: 配置各平台 Cookie/Token"
echo "  参考: 项目根目录 README.md"
echo "========================================"
