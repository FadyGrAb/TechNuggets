# Install SecretManager module.
# https://www.powershellgallery.com/packages/Microsoft.PowerShell.SecretStore/1.0.6

Install-Module -Name Microsoft.PowerShell.SecretStore

# Setup SecretManager with default configurations.
Set-SecretStoreConfiguration -PasswordTimeout 1

# Install SecretManagement module.
# https://www.powershellgallery.com/packages/Microsoft.PowerShell.SecretManagement/1.1.2

Install-Module -Name Microsoft.PowerShell.SecretManagement

# Register secret vaults.
# Register a default secret store for the SecretManagement Module.
Register-SecretVault -Name MyVault -ModuleName Microsoft.Powershell.SecretStore -DefaultVault
# Register a second vault for AWS credentials.
Register-SecretVault -Name AWSVault -ModuleName Microsoft.PowerShell.SecretStore
# Sanity check.
Get-SecretVault

# Generate a random encryption key and store in the default vault
# Create a set of allowed characters.
$chars = ("a".."z") + ("A".."Z") + (0..9) + "@#%[]{}=+"
$mykey = ""
(1..16) | ForEach-Object { $myKey += $chars | Get-Random }

Set-Secret -Vault MyVault -Name AWS_ENCRYPTION_KEY -Secret $myKey
# Sanity check
Write-Host "My generated key: $myKey"
Write-Host "My key from the vault: $(Get-Secret -Vault MyVault -Name AWS_ENCRYPTION_KEY -AsPlainText)"

# Parse my AWS Credentials from JSON
$myCredentials = Get-Content .\MyCredentials.json | ConvertFrom-Json -AsHashtable
Write-Host "AWS ACCESS KEY ID: $($myCredentials.AWS_ACCESS_KEY_ID)"
Write-Host "AWS SECRET ACCESS KEY: $($myCredentials.AWS_SECRET_ACCESS_KEY)"

# For additional security, will encrypt the credentials with the previously generated key
$encryptionKey = Get-Secret -Vault MyVault -Name AWS_ENCRYPTION_KEY # secure string

$awsAccessKeyIDSecure = ConvertTo-SecureString -String ($myCredentials.AWS_ACCESS_KEY_ID) -AsPlainText
$awsAccessKeyIDEncrypted = ConvertFrom-SecureString $awsAccessKeyIDSecure -SecureKey $encryptionKey   # Normal string but encrypted
Write-Host "Encrypted AWS_ACCESS_KEY_ID: $awsAccessKeyIDEncrypted"

$awsSecretAccessKey = ConvertTo-SecureString -String ($myCredentials.AWS_SECRET_ACCESS_KEY) -AsPlainText
$awsSecretAccessKeyEncrypted = ConvertFrom-SecureString $awsSecretAccessKey -SecureKey $encryptionKey
Write-Host "Encrypted AWS_ACCESS_KEY_ID: $awsSecretAccessKeyEncrypted"

# Store the encrypted credentials in the AWS vault
Set-Secret -Vault AWSVault -Name AWS_ACCESS_KEY_ID -Secret $awsAccessKeyIDEncrypted
Set-Secret -Vault AWSVault -Name AWS_SECRET_ACCESS_KEY -Secret $awsSecretAccessKeyEncrypted

# Retreive the secrets back from the AWS vault
$awsAccessKeyIDVault = Get-Secret -Vault AWSVault -Name AWS_ACCESS_KEY_ID -AsPlainText
$awsSecretAccessKeyVault = Get-Secret -Vault AWSVault -Name AWS_SECRET_ACCESS_KEY -AsPlainText

Write-Host "ENCRYPTED AWS ACCESS KEY ID: $awsAccessKeyIDVault"
Write-Host "ENCRYPTED AWS SECRET ACCESS KEY: $awsSecretAccessKeyVault"

# Decrypt the credentials.
$awsAccessKeyIDSecure = ConvertTo-SecureString $awsAccessKeyIDVault -SecureKey $encryptionKey                         # Secure string but decrypted.
$awsAccessKeyIDDecrypted = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($awsAccessKeyIDSecure)  # Allocates the secure string to an unmanaged Binary string in memory.
$awsAccessKeyIDDecrypted = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($awsAccessKeyIDDecrypted)  # Allocates the unmanged binary string to a managed string in memory.

$awsSecretAccessKeySecure = ConvertTo-SecureString $awsSecretAccessKeyVault -SecureKey $encryptionKey
$awsSecretAccessKeyDecrypted = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($awsSecretAccessKeySecure)
$awsSecretAccessKeyDecrypted = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($awsSecretAccessKeyDecrypted)
# Sanity check
Write-Host "AWS_ACCESS_KEY_ID: $awsAccessKeyIDDecrypted`nAWS_SECRET_ACCESS_KEY: $awsSecretAccessKeyDecrypted"

function Get-AWSAccessKeyID {
    $encryptionKey = Get-Secret -Vault MyVault -Name AWS_ENCRYPTION_KEY
    $awsAccessKeyIDVault = Get-Secret -Vault AWSVault -Name AWS_ACCESS_KEY_ID -AsPlainText

    $awsAccessKeyIDSecure = ConvertTo-SecureString $awsAccessKeyIDVault -SecureKey $encryptionKey
    $awsAccessKeyIDDecrypted = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($awsAccessKeyIDSecure)
    $awsAccessKeyIDDecrypted = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($awsAccessKeyIDDecrypted)
    return $awsAccessKeyIDDecrypted
}

function Get-AWSSecretAccessKey {
    $encryptionKey = Get-Secret -Vault MyVault -Name AWS_ENCRYPTION_KEY
    $awsSecretAccessKeyVault = Get-Secret -Vault AWSVault -Name AWS_SECRET_ACCESS_KEY -AsPlainText

    $awsSecretAccessKeySecure = ConvertTo-SecureString $awsSecretAccessKeyVault -SecureKey $encryptionKey
    $awsSecretAccessKeyDecrypted = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($awsSecretAccessKeySecure)
    $awsSecretAccessKeyDecrypted = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($awsSecretAccessKeyDecrypted)
    return $awsSecretAccessKeyDecrypted
}

Get-AWSAccessKeyID
Get-AWSSecretAccessKey
