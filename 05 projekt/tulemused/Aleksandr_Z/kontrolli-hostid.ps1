[CmdletBinding()]
param(
    [string]$InputFile = "hostid.csv"
)

function Test-HostStatus {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$HostName,
        [int]$Port = 0
    )

    try {
        if ($Port -gt 0) {
            # TCP проверка
            $r = Test-NetConnection -ComputerName $HostName -Port $Port `
                                    -WarningAction SilentlyContinue -ErrorAction Stop

            return [PSCustomObject]@{
                Olek        = if ($r.TcpTestSucceeded) { "OK" } else { "FAIL" }
                Viivitus_ms = $r.PingReplyDetails.RoundtripTime
            }
        }
        else {
            # ICMP ping
            $ping = Test-Connection -ComputerName $HostName -Count 1 -ErrorAction Stop

            return [PSCustomObject]@{
                Olek        = "OK"
                Viivitus_ms = $ping.ResponseTime
            }
        }
    }
    catch {
        return [PSCustomObject]@{
            Olek        = "FAIL"
            Viivitus_ms = $null
        }
    }
}

# --- проверка файла ---
if (!(Test-Path $InputFile)) {
    Write-Error "Файл не найден: $InputFile"
    exit 1
}

$hosts = Import-Csv -Path $InputFile

Write-Host "Kontrollin $($hosts.Count) hosti..." -ForegroundColor Cyan
Write-Host ""

$tulemus = foreach ($h in $hosts) {

    $port = if ($h.port) { [int]$h.port } else { 0 }

    # ⚠️ ВАЖНО: используем HostName, а не Host
    $test = Test-HostStatus -HostName $h.host -Port $port

    $color = if ($test.Olek -eq "OK") { "Green" } else { "Red" }

    Write-Host ("  {0,-15} {1,-25} {2,-5} {3}" -f `
        $h.nimi,
        $h.host,
        $test.Olek,
        $(if ($test.Viivitus_ms) { "$($test.Viivitus_ms) ms" } else { "-" })
    ) -ForegroundColor $color

    [PSCustomObject]@{
        Nimi         = $h.nimi
        Host         = $h.host
        Port         = $h.port
        Olek         = $test.Olek
        Viivitus_ms  = $test.Viivitus_ms
        Kontrollitud = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        Kirjeldus    = $h.kirjeldus
    }
}

# --- сохранение CSV ---
$kuupäev = Get-Date -Format "yyyy-MM-dd"
$fail = "saadavus_$kuupäev.csv"

$tulemus | Export-Csv -Path $fail -NoTypeInformation -Encoding UTF8

# --- статистика ---
$ok = ($tulemus | Where-Object Olek -eq "OK").Count
$failCount = ($tulemus | Where-Object Olek -eq "FAIL").Count

Write-Host ""
Write-Host "Kokkuvõte: $ok / $($tulemus.Count) OK, $failCount maas" -ForegroundColor Cyan
Write-Host "Tulemus salvestatud: $fail" -ForegroundColor Cyan