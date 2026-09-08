$ErrorActionPreference = "Stop"

param(
    [Parameter(Mandatory = $true)]
    [string]$SecretsPath
)

. "$PSScriptRoot\securecode_crypto.ps1"

$json = Read-SecureCodeSecretsDpapiJson -SecretsPath $SecretsPath
Write-Output $json
