# 龙虾MCP - API密钥快速配置脚本 v1.0
# 以管理员身份运行此脚本
# 用法: 右键 → 以管理员身份运行 PowerShell → .\setup_api_keys.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  龙虾MCP API密钥自动配置" -ForegroundColor Cyan
Write-Host "  BRAVE_API_KEY + ALIYUN_REFRESH_TOKEN" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --------------------------------------------------
# Step 1: Brave Search API Key
# --------------------------------------------------
Write-Host "[1/2] Brave Search API Key" -ForegroundColor Yellow
Write-Host "  正在打开申请页面: https://api.search.brave.com/app/keys"
Start-Process "https://api.search.brave.com/app/keys"

do {
    $braveKey = Read-Host "  粘贴 Brave API Key (或输入 skip 跳过):"
    if ($braveKey -eq "skip") { break }
    if ($braveKey -notmatch "^[a-fA-F0-9]{32,}$") {
        Write-Host "  ⚠️ 格式不对（应为32位以上十六进制），请检查" -ForegroundColor Red
    }
} while ($braveKey -notmatch "^[a-fA-F0-9]{32,}$")

if ($braveKey -ne "skip" -and $braveKey) {
    [Environment]::SetEnvironmentVariable("BRAVE_API_KEY", $braveKey, "User")
    Write-Host "  ✅ BRAVE_API_KEY 已写入用户环境变量" -ForegroundColor Green
} else {
    Write-Host "  ⏭️ 跳过" -ForegroundColor Gray
}

Write-Host ""

# --------------------------------------------------
# Step 2: 阿里云盘 Refresh Token
# --------------------------------------------------
Write-Host "[2/2] 阿里云盘 Refresh Token" -ForegroundColor Yellow
Write-Host "  正在打开授权页面..."
Start-Process "https://www.aliyundrive.com/oauth/authorize?client_id=263610&response_type=code&redirect_uri=https://api.aliyundrive.com/oauth/authorize/callback&scope=user:base,file:all:read,file:all:write"
Write-Host "  用阿里云盘App扫码，获取 refresh_token"

do {
    $aliToken = Read-Host "  粘贴阿里云 Refresh Token (或输入 skip 跳过):"
    if ($aliToken -eq "skip") { break }
    if ($aliToken.Length -lt 50) {
        Write-Host "  ⚠️ 长度不足（需50字符以上），请检查" -ForegroundColor Red
    }
} while ($aliToken.Length -lt 50)

if ($aliToken -ne "skip" -and $aliToken) {
    [Environment]::SetEnvironmentVariable("ALIYUN_REFRESH_TOKEN", $aliToken, "User")
    Write-Host "  ✅ ALIYUN_REFRESH_TOKEN 已写入用户环境变量" -ForegroundColor Green
} else {
    Write-Host "  ⏭️ 跳过" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  配置完成！" -ForegroundColor Green
Write-Host "  接下来运行 auto_fill_credentials.ps1" -ForegroundColor Green
Write-Host "  即可一键替换所有MCP配置" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Read-Host "按Enter退出"