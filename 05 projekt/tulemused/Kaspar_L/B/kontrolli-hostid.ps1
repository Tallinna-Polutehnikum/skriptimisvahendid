$hostid = Import-Csv -Path "hostid.csv"

$hostid | Format-Table nimi, host, port -AutoSize

function Test-HostStatus {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
    [string]$HostName,
        [int]$Port = 0
    )

    try {
        if ($Port -gt 0) {
            # TCP — kontrollib kindlalt porti
            $r = Test-NetConnection -ComputerName $HostName -Port $Port `
                                    -WarningAction SilentlyContinue -ErrorAction Stop
            return [PSCustomObject]@{
                Olek        = if ($r.TcpTestSucceeded) { "OK" } else { "FAIL" }
                Viivitus_ms = if ($r.PingReplyDetails) { $r.PingReplyDetails.RoundtripTime } else { $null }
            }
        }
        else {
            # ICMP — tavaline ping
            $r = Test-Connection -ComputerName $HostName -Count 1 -Quiet -ErrorAction Stop
            $v = (Test-Connection -ComputerName $HostName -Count 1 -ErrorAction Stop).ResponseTime
            return [PSCustomObject]@{
                Olek        = if ($r) { "OK" } else { "FAIL" }
                Viivitus_ms = $v
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

$tulemus = foreach ($h in $hostid) {
    $port = if ($h.port) { [int]$h.port } else { 0 }
    $test = Test-HostStatus -HostName $h.host -Port $port

    [PSCustomObject]@{
        Nimi          = $h.nimi
        Host          = $h.host
        Port          = $h.port
        Olek          = $test.Olek
        Viivitus_ms   = $test.Viivitus_ms
        Kontrollitud  = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        Kirjeldus     = $h.kirjeldus
    }

    # Kuva progress
    $värv = if ($test.Olek -eq "OK") { "Green" } else { "Red" }
    Write-Host ("  {0,-15} {1,-25} {2,-5} {3} ms" -f `
        $h.nimi, $h.host, $test.Olek, $test.Viivitus_ms) `
        -ForegroundColor $värv
}

$kuupäev = Get-Date -Format "yyyy-MM-dd"
$failinimi = "saadavus_$kuupäev.csv"

$tulemus | Export-Csv -Path $failinimi -NoTypeInformation -Encoding UTF8

$ok   = ($tulemus | Where-Object Olek -eq "OK").Count
$fail = ($tulemus | Where-Object Olek -eq "FAIL").Count

Write-Host ""
Write-Host "Kokkuvõte: $ok / $($tulemus.Count) OK, $fail maas" -ForegroundColor Cyan
Write-Host "Tulemus salvestatud: $failinimi" -ForegroundColor Cyan