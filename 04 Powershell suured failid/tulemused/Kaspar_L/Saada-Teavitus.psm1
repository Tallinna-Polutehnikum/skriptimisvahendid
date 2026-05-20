function Send-AlertMessage {
<#
.SYNOPSIS
    Saadab teavituse Discordi webhooki kaudu.

.DESCRIPTION
    Send-AlertMessage saadab sõnumi Discordi kanalisse webhook URL-i abil.
    Webhook URL loetakse failist config.psd1.

.PARAMETER Message
    Teate tekst.

.PARAMETER Severity
    Teate raskusaste: Info, Warning või Critical.

.PARAMETER Source
    Allika nimi (nt arvuti nimi).
#>

    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Message,

        [ValidateSet("Info","Warning","Critical")]
        [string]$Severity = "Info",

        [string]$Source = $env:COMPUTERNAME
    )

    # Webhook URL
    
    $configPath = Join-Path $PSScriptRoot "config.psd1"
    $config = Import-PowerShellDataFile $configPath
    
    $url = $config.WebhookUrl
    if (-not $url) {
        throw "Webhook URL puudub."
    }

    # Logid
    $logPath = Join-Path $env:TEMP "ps-alerts.log"
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    # Discord värvid
    $color = switch ($Severity) {
        "Info"     { 3447003 }
        "Warning"  { 16776960 }
        "Critical" { 15158332 }
    }

    # Discord payload
    $json = @{
        username = "PS-Monitor"
        embeds = @(@{
            title       = "[$Severity] $Source"
            description = $Message
            color       = $color
            timestamp   = (Get-Date).ToString("o")
        })
    } | ConvertTo-Json -Depth 4

    try {
        Invoke-RestMethod -Uri $url -Method Post -Body $json -ContentType "application/json" -ErrorAction Stop

        Write-Verbose "Teade saadetud: $Message"
        Add-Content $logPath "$time [OK]   $Severity | $Source | $Message"
    }
    catch {
        Write-Warning "Discordi saatmine ebaõnnestus: $($_.Exception.Message)"
        Add-Content $logPath "$time [FAIL] $Severity | $Source | $Message | $($_.Exception.Message)"
    }
}

Export-ModuleMember -Function Send-AlertMessage