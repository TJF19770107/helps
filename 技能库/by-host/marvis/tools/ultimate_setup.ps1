# 龙虾MCP 终极凭据补全脚本 v2.2
# UTF-8 BOM encoded - PS 5.1 compatible
# 管理员身份运行 PowerShell 执行此脚本
$ErrorActionPreference = "Continue"

$configPath = "C:\Users\Administrator\WorkBuddy\2026-05-22-task-3\lobster_mcp\cc_switch_import.json"
Add-Type -AssemblyName System.Windows.Forms

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LobsterMCP Ultimate Setup v2.2       " -ForegroundColor Cyan
Write-Host "  WECHAT + BRAVE + ALIYUN              " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# ============================================================
# [0/4] Playwright dependency check
# ============================================================
Write-Host "`n[0/4] Checking Playwright..." -ForegroundColor Cyan
$pyCheck = & "E:\VNPY\python.exe" -c "from playwright.sync_api import sync_playwright; print('OK')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Installing playwright..." -ForegroundColor Yellow
    & "E:\VNPY\python.exe" -m pip install playwright 2>&1 | Out-Null
    & "E:\VNPY\python.exe" -m playwright install chromium 2>&1 | Out-Null
}
Write-Host "  [OK] Playwright ready" -ForegroundColor Green

# ============================================================
# [1/4] WeChat Video Cookie - QR scan login
# ============================================================
Write-Host "`n[1/4] WECHAT_VIDEO_COOKIE" -ForegroundColor Yellow
Write-Host "  Opening Edge browser, scan QR code with WeChat..."

$pyTemp = Join-Path $env:TEMP "wx_login.py"
@'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=False)
    page = browser.new_page()
    page.goto("https://channels.weixin.qq.com/")
    print(">>> Scan QR code with WeChat, then press Enter <<<", flush=True)
    input()
    cookies = page.context.cookies("https://channels.weixin.qq.com")
    cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    print(f"COOKIE_START{cookie_str}COOKIE_END", flush=True)
    browser.close()
'@ | Set-Content $pyTemp -Encoding UTF8

$out = & "E:\VNPY\python.exe" $pyTemp 2>&1
Remove-Item $pyTemp -Force -ErrorAction SilentlyContinue

if ($out -match "COOKIE_START(.*?)COOKIE_END") {
    $wc = $matches[1]
    Write-Host "  [OK] Got cookie ($($wc.Length) chars)" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Could not get cookie" -ForegroundColor Red
    $wc = $null
}

# ============================================================
# [2/4] BRAVE_API_KEY - clipboard auto-read
# ============================================================
Write-Host "`n[2/4] BRAVE_API_KEY" -ForegroundColor Yellow
Write-Host "  Copy your Brave API Key to clipboard now..."

$bk = $null
$to = 0
while ($to -lt 60 -and -not $bk) {
    try { $clip = [System.Windows.Forms.Clipboard]::GetText() } catch { $clip = "" }
    if ($clip -match "^[a-fA-F0-9]{32,}$") { $bk = $clip }
    if (-not $bk) { Start-Sleep 2; $to += 2 }
}

if ($bk) {
    setx BRAVE_API_KEY "$bk" | Out-Null
    $env:BRAVE_API_KEY = $bk
    Write-Host "  [OK] BRAVE_API_KEY written to env var" -ForegroundColor Green
} else {
    Write-Host "  [SKIP] Timeout, no key detected" -ForegroundColor Red
}

# ============================================================
# [3/4] ALIYUN_REFRESH_TOKEN - clipboard auto-read
# ============================================================
Write-Host "`n[3/4] ALIYUN_REFRESH_TOKEN" -ForegroundColor Yellow
Write-Host "  Copy your Aliyun Refresh Token to clipboard..."

$at = $null
$to = 0
while ($to -lt 60 -and -not $at) {
    try { $clip = [System.Windows.Forms.Clipboard]::GetText() } catch { $clip = "" }
    if ($clip.Length -ge 50) { $at = $clip }
    if (-not $at) { Start-Sleep 2; $to += 2 }
}

if ($at) {
    setx ALIYUN_REFRESH_TOKEN "$at" | Out-Null
    $env:ALIYUN_REFRESH_TOKEN = $at
    Write-Host "  [OK] ALIYUN_REFRESH_TOKEN written to env var" -ForegroundColor Green
} else {
    Write-Host "  [SKIP] Timeout, no token detected" -ForegroundColor Red
}

# ============================================================
# [4/4] Replace JSON placeholders (exact match)
# ============================================================
Write-Host "`n[4/4] Updating cc_switch_import.json..." -ForegroundColor Cyan

$content = Get-Content $configPath -Raw -Encoding UTF8

# Exact placeholder text from the JSON file
$pWechat = '请填写: 登录channels.weixin.qq.com后F12→Application→Cookies'
$pBrave  = '请填写: https://api.search.brave.com 申请免费APIKey'
$pAliyun = '请填写: 阿里云盘App→我的→扫码登录PC→从本地配置文件获取'

if ($wc) { $content = $content -replace ([regex]::Escape($pWechat)), $wc }
if ($bk) { $content = $content -replace ([regex]::Escape($pBrave)), $bk }
if ($at) { $content = $content -replace ([regex]::Escape($pAliyun)), $at }

Set-Content $configPath $content -Encoding UTF8

# ============================================================
# Summary
# ============================================================
$rem = ([regex]::Matches((Get-Content $configPath -Raw -Encoding UTF8), "请填写")).Count

if ($wc) { $s1 = "[OK]" } else { $s1 = "[--]" }
if ($bk) { $s2 = "[OK]" } else { $s2 = "[--]" }
if ($at) { $s3 = "[OK]" } else { $s3 = "[--]" }

Write-Host ""
Write-Host "========================================"
Write-Host "  RESULT SUMMARY:"
Write-Host "  WECHAT_VIDEO_COOKIE : $s1"
Write-Host "  BRAVE_API_KEY       : $s2"
Write-Host "  ALIYUN_REFRESH_TOKEN: $s3"
Write-Host "  Remaining placeholders: $rem"
Write-Host ""
Write-Host "Next: CC Switch -> Settings -> MCP -> Import Config" -ForegroundColor Cyan
Read-Host "`nPress Enter to exit"
