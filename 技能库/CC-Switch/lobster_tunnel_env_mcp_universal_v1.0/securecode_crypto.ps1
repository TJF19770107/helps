$ErrorActionPreference = "Stop"

function New-SecureRandomBase64 {
    <#
    .SYNOPSIS
    Generates cryptographically-secure random bytes and returns base64.
    #>
    param(
        [Parameter(Mandatory = $true)]
        [int]$ByteCount
    )

    $bytes = New-Object byte[] $ByteCount
    [System.Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
    return [Convert]::ToBase64String($bytes)
}

function New-StrongToken {
    <#
    .SYNOPSIS
    Generates a high-entropy bearer token string (URL-safe).
    #>
    param(
        [Parameter(Mandatory = $false)]
        [int]$ByteCount = 48
    )

    $b64 = New-SecureRandomBase64 -ByteCount $ByteCount
    $token = $b64.Replace("+", "-").Replace("/", "_").TrimEnd("=")
    return $token
}

function New-RsaKeyPairPem {
    <#
    .SYNOPSIS
    Generates RSA keypair and returns PEM strings.
    #>
    param(
        [Parameter(Mandatory = $false)]
        [int]$KeySize = 4096
    )

    $rsa = [System.Security.Cryptography.RSA]::Create($KeySize)
    try {
        $priv = $rsa.ExportPkcs8PrivateKey()
        $pub = $rsa.ExportSubjectPublicKeyInfo()

        $privPem = -join ([System.Security.Cryptography.PemEncoding]::Write("PRIVATE KEY", $priv))
        $pubPem = -join ([System.Security.Cryptography.PemEncoding]::Write("PUBLIC KEY", $pub))

        return @{
            PrivateKeyPem = $privPem
            PublicKeyPem  = $pubPem
        }
    } finally {
        $rsa.Dispose()
    }
}

function New-SelfSignedTlsPem {
    <#
    .SYNOPSIS
    Generates a self-signed TLS certificate (RSA) and returns cert/key PEM.
    #>
    param(
        [Parameter(Mandatory = $false)]
        [string]$Subject = "CN=securecode-mcp.local",
        [Parameter(Mandatory = $false)]
        [string[]]$DnsNames = @("localhost", "securecode-mcp.local"),
        [Parameter(Mandatory = $false)]
        [int]$KeySize = 4096,
        [Parameter(Mandatory = $false)]
        [int]$ValidDays = 825
    )

    $rsa = [System.Security.Cryptography.RSA]::Create($KeySize)
    try {
        $hashAlg = [System.Security.Cryptography.HashAlgorithmName]::SHA256
        $sigPad = [System.Security.Cryptography.RSASignaturePadding]::Pkcs1
        $req = [System.Security.Cryptography.X509Certificates.CertificateRequest]::new($Subject, $rsa, $hashAlg, $sigPad)

        $san = [System.Security.Cryptography.X509Certificates.SubjectAlternativeNameBuilder]::new()
        foreach ($d in $DnsNames) { $san.AddDnsName($d) }
        $req.CertificateExtensions.Add($san.Build())

        $ku = [System.Security.Cryptography.X509Certificates.X509KeyUsageFlags]::DigitalSignature -bor `
            [System.Security.Cryptography.X509Certificates.X509KeyUsageFlags]::KeyEncipherment
        $req.CertificateExtensions.Add([System.Security.Cryptography.X509Certificates.X509KeyUsageExtension]::new($ku, $false))

        $eku = [System.Security.Cryptography.OidCollection]::new()
        $eku.Add([System.Security.Cryptography.Oid]::new("1.3.6.1.5.5.7.3.1")) | Out-Null
        $req.CertificateExtensions.Add([System.Security.Cryptography.X509Certificates.X509EnhancedKeyUsageExtension]::new($eku, $false))

        $notBefore = [DateTimeOffset]::UtcNow.AddMinutes(-5)
        $notAfter = $notBefore.AddDays($ValidDays)
        $cert = $req.CreateSelfSigned($notBefore, $notAfter)
        try {
            $certDer = $cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert)
            $certPem = -join ([System.Security.Cryptography.PemEncoding]::Write("CERTIFICATE", $certDer))

            $priv = $rsa.ExportPkcs8PrivateKey()
            $keyPem = -join ([System.Security.Cryptography.PemEncoding]::Write("PRIVATE KEY", $priv))

            return @{
                CertPem = $certPem
                KeyPem  = $keyPem
            }
        } finally {
            $cert.Dispose()
        }
    } finally {
        $rsa.Dispose()
    }
}

function Protect-BytesDpapi {
    <#
    .SYNOPSIS
    Protects bytes via DPAPI CurrentUser scope.
    #>
    param(
        [Parameter(Mandatory = $true)]
        [byte[]]$Bytes
    )

    return [System.Security.Cryptography.ProtectedData]::Protect(
        $Bytes,
        $null,
        [System.Security.Cryptography.DataProtectionScope]::CurrentUser
    )
}

function Unprotect-BytesDpapi {
    <#
    .SYNOPSIS
    Unprotects bytes via DPAPI CurrentUser scope.
    #>
    param(
        [Parameter(Mandatory = $true)]
        [byte[]]$Bytes
    )

    return [System.Security.Cryptography.ProtectedData]::Unprotect(
        $Bytes,
        $null,
        [System.Security.Cryptography.DataProtectionScope]::CurrentUser
    )
}

function Save-SecureCodeSecretsDpapi {
    <#
    .SYNOPSIS
    Creates/rotates SecureCode secrets and stores them as DPAPI-encrypted JSON.
    #>
    param(
        [Parameter(Mandatory = $true)]
        [string]$SecretsPath
    )

    $dir = Split-Path -Parent $SecretsPath
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }

    $aesKeyB64 = New-SecureRandomBase64 -ByteCount 32
    $rsaPair = New-RsaKeyPairPem -KeySize 4096
    $token = New-StrongToken -ByteCount 48
    $tls = New-SelfSignedTlsPem

    $payload = @{
        version         = 1
        createdAtUtc    = [DateTime]::UtcNow.ToString("o")
        aesKeyB64       = $aesKeyB64
        rsaPrivateKeyPem = $rsaPair.PrivateKeyPem
        rsaPublicKeyPem  = $rsaPair.PublicKeyPem
        mcpBearerToken  = $token
        tlsCertPem      = $tls.CertPem
        tlsKeyPem       = $tls.KeyPem
    } | ConvertTo-Json -Depth 6

    $plain = [System.Text.Encoding]::UTF8.GetBytes($payload)
    $prot = Protect-BytesDpapi -Bytes $plain
    [System.IO.File]::WriteAllBytes($SecretsPath, $prot)

    return @{
        SecretsPath = $SecretsPath
        CreatedAtUtc = [DateTime]::UtcNow.ToString("o")
    }
}

function Read-SecureCodeSecretsDpapiJson {
    <#
    .SYNOPSIS
    Decrypts the DPAPI secrets file and returns the plaintext JSON string.
    #>
    param(
        [Parameter(Mandatory = $true)]
        [string]$SecretsPath
    )

    if (-not (Test-Path $SecretsPath)) { throw "Secrets file not found: $SecretsPath" }
    $prot = [System.IO.File]::ReadAllBytes($SecretsPath)
    $plain = Unprotect-BytesDpapi -Bytes $prot
    return [System.Text.Encoding]::UTF8.GetString($plain)
}

function Set-FileAclCurrentUserOnly {
    <#
    .SYNOPSIS
    Restricts file ACL to current user only (best-effort).
    #>
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

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
