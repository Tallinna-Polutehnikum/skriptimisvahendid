[CmdletBinding()]
param(
    [string]$Sisend = "hostid.csv",
    [string]$ValjundKaust = "."
)

function Test-HostStatus {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$HostName,

        [int]$Port = 0
    )

    try {
        $r = Test-Connection -TargetName $HostName -Count 1 -ErrorAction Stop

        return [PSCustomObject]@{
            Olek = "OK"
            Viivitus_ms = [math]::Round($r.Latency, 0)
        }
    }
    catch {
        return [PSCustomObject]@{
            Olek = "FAIL"
            Viivitus_ms = $null
        }
    }
}

if (-not (Test-Path $Sisend)) {
    Write-Host "Sisendfaili ei leitud: $Sisend" -ForegroundColor Red
    exit 1
}

$hostid = Import-Csv -Path $Sisend

Write-Host "Kontrollin $($hostid.Count) hosti..."
Write-Host ""

$tulemus = foreach ($h in $hostid) {
    $port = if ($h.port) { [int]$h.port } else { 0 }
    $test = Test-HostStatus -HostName $h.host -Port $port

    $viivitus = if ($test.Viivitus_ms) { "$($test.Viivitus_ms) ms" } else { "-" }

    if ($port -gt 0) {
        $kuvatavHost = "$($h.host):$port"
    }
    else {
        $kuvatavHost = $h.host
    }

    $varv = if ($test.Olek -eq "OK") { "Green" } else { "Red" }

    Write-Host ("  {0,-15} {1,-28} {2,-5} {3}" -f $h.nimi, $kuvatavHost, $test.Olek, $viivitus) -ForegroundColor $varv

    [PSCustomObject]@{
        Nimi = $h.nimi
        Host = $h.host
        Port = $h.port
        Olek = $test.Olek
        Viivitus_ms = $test.Viivitus_ms
        Kontrollitud = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        Kirjeldus = $h.kirjeldus
    }
}

$kuupaev = Get-Date -Format "yyyy-MM-dd"
$failinimi = Join-Path $ValjundKaust "saadavus_$kuupaev.csv"

$tulemus | Export-Csv -Path $failinimi -NoTypeInformation -Encoding UTF8

$ok = ($tulemus | Where-Object Olek -eq "OK").Count
$fail = ($tulemus | Where-Object Olek -eq "FAIL").Count

Write-Host ""
Write-Host "Kokkuvõte: $ok / $($tulemus.Count) OK, $fail maas" -ForegroundColor Cyan
Write-Host "Tulemus salvestatud: $failinimi" -ForegroundColor Cyan