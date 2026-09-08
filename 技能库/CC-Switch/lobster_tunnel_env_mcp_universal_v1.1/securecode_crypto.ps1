$ErrorActionPreference = "Stop"

try { Add-Type -AssemblyName System.Security } catch {}

function New-SecureRandomBase64 {
    param([Parameter(Mandatory = $true)][int]$ByteCount)
    $bytes = New-Object byte[] $ByteCount
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try {
        $rng.GetBytes($bytes)
    } finally {
        $rng.Dispose()
    }
    [Convert]::ToBase64String($bytes)
}

function New-StrongToken {
    param([int]$ByteCount = 48)
    $b64 = New-SecureRandomBase64 -ByteCount $ByteCount
    $b64.Replace("+", "-").Replace("/", "_").TrimEnd("=")
}

function New-RsaKeyPairPem {
    param([int]$KeySize = 4096)
    $rsa = [System.Security.Cryptography.RSA]::Create($KeySize)
    try {
        $priv = $rsa.ExportPkcs8PrivateKey()
        $pub = $rsa.ExportSubjectPublicKeyInfo()
        $privPem = -join ([System.Security.Cryptography.PemEncoding]::Write("PRIVATE KEY", $priv))
        $pubPem = -join ([System.Security.Cryptography.PemEncoding]::Write("PUBLIC KEY", $pub))
        @{ PrivateKeyPem = $privPem; PublicKeyPem = $pubPem }
    } finally {
        $rsa.Dispose()
    }
}

function Protect-BytesDpapi {
    param([Parameter(Mandatory = $true)][byte[]]$Bytes)
    [System.Security.Cryptography.ProtectedData]::Protect(
        $Bytes,
        $null,
        [System.Security.Cryptography.DataProtectionScope]::CurrentUser
    )
}

function Unprotect-BytesDpapi {
    param([Parameter(Mandatory = $true)][byte[]]$Bytes)
    [System.Security.Cryptography.ProtectedData]::Unprotect(
        $Bytes,
        $null,
        [System.Security.Cryptography.DataProtectionScope]::CurrentUser
    )
}

function Set-FileAclCurrentUserOnly {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (-not (Test-Path $Path)) { return }
    try {
        $me = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        $acl = Get-Acl $Path
        $acl.SetAccessRuleProtection($true, $false)
        $acl.Access | ForEach-Object { $acl.RemoveAccessRule($_) | Out-Null }
        $rule = New-Object System.Security.AccessControl.FileSystemAccessRule($me, "FullControl", "Allow")
        $acl.AddAccessRule($rule) | Out-Null
        Set-Acl -Path $Path -AclObject $acl
    } catch {
    }
}

function Get-CertSha256Fingerprint {
    param([Parameter(Mandatory = $true)][System.Security.Cryptography.X509Certificates.X509Certificate2]$Cert)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $hash = $sha.ComputeHash($Cert.RawData)
        ($hash | ForEach-Object { $_.ToString("x2") }) -join ""
    } finally {
        $sha.Dispose()
    }
}

function New-OrGet-SecureCodeMcpCertificate {
    param(
        [Parameter(Mandatory = $true)][string]$FriendlyNamePrefix,
        [Parameter(Mandatory = $false)][string]$Subject = "CN=securecode-mcp.local",
        [Parameter(Mandatory = $false)][int]$ValidDays = 825
    )

    $storePath = "Cert:\CurrentUser\My"
    $existing = Get-ChildItem $storePath | Where-Object { $_.FriendlyName -like ($FriendlyNamePrefix + "*") } | Select-Object -First 1
    if ($existing) { return $existing }

    $notAfter = (Get-Date).AddDays($ValidDays)
    $cert = New-SelfSignedCertificate `
        -Subject $Subject `
        -KeyAlgorithm RSA `
        -KeyLength 4096 `
        -KeyExportPolicy NonExportable `
        -CertStoreLocation $storePath `
        -FriendlyName ($FriendlyNamePrefix + "-" + (Get-Date).ToString("yyyyMMdd_HHmmss")) `
        -NotAfter $notAfter `
        -KeyUsage DigitalSignature, KeyEncipherment `
        -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1")

    $cert
}

function Save-SecureCodeSecretsDpapi {
    param(
        [Parameter(Mandatory = $true)][string]$SecretsPath,
        [Parameter(Mandatory = $true)][System.Security.Cryptography.X509Certificates.X509Certificate2]$Cert
    )

    $dir = Split-Path -Parent $SecretsPath
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }

    $aesKeyB64 = New-SecureRandomBase64 -ByteCount 32
    $rsaPair = New-RsaKeyPairPem -KeySize 4096
    $token = New-StrongToken -ByteCount 48

    $payload = @{
        version          = 1
        createdAtUtc     = [DateTime]::UtcNow.ToString("o")
        aesKeyB64        = $aesKeyB64
        rsaPrivateKeyPem = $rsaPair.PrivateKeyPem
        rsaPublicKeyPem  = $rsaPair.PublicKeyPem
        mcpBearerToken   = $token
        certThumbprint   = $Cert.Thumbprint
        certSha256       = Get-CertSha256Fingerprint -Cert $Cert
    } | ConvertTo-Json -Depth 6

    $plain = [System.Text.Encoding]::UTF8.GetBytes($payload)
    $prot = Protect-BytesDpapi -Bytes $plain
    [System.IO.File]::WriteAllBytes($SecretsPath, $prot)
    Set-FileAclCurrentUserOnly -Path $SecretsPath
}

function Read-SecureCodeSecretsDpapiJson {
    param([Parameter(Mandatory = $true)][string]$SecretsPath)
    if (-not (Test-Path $SecretsPath)) { throw "Secrets file not found: $SecretsPath" }
    $prot = [System.IO.File]::ReadAllBytes($SecretsPath)
    $plain = Unprotect-BytesDpapi -Bytes $prot
    [System.Text.Encoding]::UTF8.GetString($plain)
}
