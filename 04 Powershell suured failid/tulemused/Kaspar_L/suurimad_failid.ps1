
[CmdletBinding()]
param(
    [string] $Path   = $HOME,
    [int]    $TopN   = 10,
    [double] $WarnGB = 1,
    [double] $CritGB = 5,
    [string] $Väljund = "suurimad_failid.csv"
)

Import-Module .\Saada-Teavitus.psm1 -Force

# CSV skriptiga samasse kausta
$baseDir = $PSScriptRoot
$outputPath = Join-Path -Path $baseDir -ChildPath $Väljund

# teavituste moodul
$moodul = Join-Path -Path $baseDir -ChildPath "Saada-Teavitus.psm1"
if (Test-Path $moodul) {
    Import-Module $moodul -Force
    $teavitusedLubatud = $true
} else {
    Write-Warning "Saada-Teavitus.psm1 puudub — jätkan ilma teavitusteta."
    $teavitusedLubatud = $false
}

# loetavaks
function Format-Suurus {
    param([long]$Baite)

    if     ($Baite -ge 1GB) { "{0:N1} GB" -f ($Baite / 1GB) }
    elseif ($Baite -ge 1MB) { "{0:N1} MB" -f ($Baite / 1MB) }
    else                    { "{0:N1} KB" -f ($Baite / 1KB) }
}

#
Write-Host "Otsin '$Path' alt $TopN kõige suuremat faili..."

$failid = Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue |
          Sort-Object -Property Length -Descending |
          Select-Object -First $TopN

# tulemus
$tulemus = foreach ($fail in $failid) {
    [PSCustomObject]@{
        Tee      = $fail.FullName
        Nimi     = $fail.Name
        Suurus   = Format-Suurus -Baite $fail.Length
        Baite    = $fail.Length
        Muudetud = $fail.LastWriteTime
    }
}

# CSV Tee, Nimi, Suurus
$tulemus |
    Select-Object Tee, Nimi, Suurus |
    Export-Csv -Path $outputPath -NoTypeInformation -Encoding UTF8

Write-Host "Salvestatud: $outputPath"

#tulemus ekraanile
$tulemus | Select-Object Nimi, Suurus, Tee | Format-Table -AutoSize

# teavitused
if ($teavitusedLubatud) {
    $warnBytes = $WarnGB * 1GB
    $critBytes = $CritGB * 1GB
    }
foreach ($fail in $tulemus) {
    $baite = (Get-Item $fail.Tee -ErrorAction SilentlyContinue).Length

    if ($baite -ge 5GB) {
        Send-AlertMessage -Message "Väga suur fail: $($fail.Nimi) ($($fail.Suurus))" -Severity Critical
    }
    elseif ($baite -ge 1GB) {
        Send-AlertMessage -Message "Suur fail: $($fail.Nimi) ($($fail.Suurus))" -Severity Warning
    }
}