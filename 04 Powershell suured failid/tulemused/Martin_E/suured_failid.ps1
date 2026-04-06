# Leia kasutaja kodukaust
$kodu = [Environment]::GetFolderPath("UserProfile")

Write-Host "Otsin faile, palun oota..."

# Kogu failid kokku (rekursiivselt)
$failid = Get-ChildItem -Path $kodu -Recurse -File -ErrorAction SilentlyContinue

# Turvaline objektide loomine
$andmed = foreach ($f in $failid) {
    try {
        [PSCustomObject]@{
            Tee    = $f.FullName
            Nimi   = $f.Name
            Suurus = $f.Length
        }
    } catch {
        continue
    }
}

# Sorteeri suuruse järgi ja võta 10 suurimat
$top10 = $andmed | Sort-Object Suurus -Descending | Select-Object -First 10

# Funktsioon suuruse muutmiseks loetavaks
function Loetav-Suurus($b) {
    if ($b -ge 1GB) { return "{0:N1} GB" -f ($b / 1GB) }
    elseif ($b -ge 1MB) { return "{0:N1} MB" -f ($b / 1MB) }
    elseif ($b -ge 1KB) { return "{0:N1} KB" -f ($b / 1KB) }
    else { return "$b B" }
}

# 1) Väljasta terminali
Write-Host "`n10 kõige suuremat faili sinu kodukaustas:`n"

foreach ($f in $top10) {
    $suurus = Loetav-Suurus $f.Suurus
    Write-Host ("{0,10} | {1}" -f $suurus, $f.Tee)
}

# 2) Salvesta CSV-fail
$valjundKaust = Join-Path -Path $PSScriptRoot -ChildPath "tulemused\Martin_E"
New-Item -ItemType Directory -Path $valjundKaust -Force | Out-Null

$csvFail = Join-Path -Path $valjundKaust -ChildPath "suured_failid.csv"

$top10 | Export-Csv -Path $csvFail -NoTypeInformation -Encoding UTF8

Write-Host "`nCSV fail salvestatud: $csvFail"