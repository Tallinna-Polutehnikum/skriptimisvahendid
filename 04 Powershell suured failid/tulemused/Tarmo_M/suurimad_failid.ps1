# 1. Leia kõik failid kodukaustast
$failid = Get-ChildItem -Path $HOME -Recurse -File -ErrorAction SilentlyContinue

# 2. Sorteeri suuruse järgi ja võta top 10
$top10 = $failid |
    Sort-Object -Property Length -Descending |
    Select-Object -First 10

# 3. Funktsioon suuruse vormindamiseks
function Vorminda-Suurus($baidid) {
    if ($baidid -ge 1GB) {
        return "{0:N1} GB" -f ($baidid / 1GB)
    }
    elseif ($baidid -ge 1MB) {
        return "{0:N1} MB" -f ($baidid / 1MB)
    }
    else {
        return "{0:N1} KB" -f ($baidid / 1KB)
    }
}

# 4. Koosta tulemused
$tulemus = foreach ($fail in $top10) {
    [PSCustomObject]@{
        Tee    = $fail.FullName
        Nimi   = $fail.Name
        Suurus = Vorminda-Suurus $fail.Length
    }
}

# 5. Salvesta CSV faili (skriptiga samasse kausta)
$valjund = Join-Path $PSScriptRoot "suurimad_failid.csv"

$tulemus | Export-Csv -Path $valjund -NoTypeInformation -Encoding UTF8

# 6. Väljasta info
Write-Host "Top 10 suurimat faili:"
$tulemus | Format-Table -AutoSize

Write-Host $valjund

# --- 0. Impordi teavituste moodul ---
Import-Module .\Saada-Teavitus.psm1 -Force


# 1. Leia kõik failid kodukaustast
$failid = Get-ChildItem -Path $HOME -Recurse -File -ErrorAction SilentlyContinue

# 2. Sorteeri suuruse järgi ja võta top 10
$top10 = $failid |
    Sort-Object -Property Length -Descending |
    Select-Object -First 10

# 3. Funktsioon suuruse vormindamiseks
function Vorminda-Suurus($baidid) {
    if ($baidid -ge 1GB) {
        return "{0:N1} GB" -f ($baidid / 1GB)
    }
    elseif ($baidid -ge 1MB) {
        return "{0:N1} MB" -f ($baidid / 1MB)
    }
    else {
        return "{0:N1} KB" -f ($baidid / 1KB)
    }
}

# 4. Koosta tulemused
$tulemus = foreach ($fail in $top10) {
    [PSCustomObject]@{
        Tee    = $fail.FullName
        Nimi   = $fail.Name
        Suurus = Vorminda-Suurus $fail.Length
        Baidid = $fail.Length   # 👉 LISATUD (vajalik kontrolliks)
    }
}

# 5. Salvesta CSV faili
$valjund = Join-Path $PSScriptRoot "suurimad_failid.csv"
$tulemus | Export-Csv -Path $valjund -NoTypeInformation -Encoding UTF8

# 6. Väljasta info
Write-Host "Top 10 suurimat faili:"
$tulemus | Format-Table -AutoSize

Write-Host $valjund


# --- 7. TEAVITUSED (UUS OSA) ---
foreach ($fail in $tulemus) {

    if ($fail.Baidid -ge 5GB) {
        Send-AlertMessage `
            -Message "VÄGA SUUR FAIL: $($fail.Nimi) ($($fail.Suurus))`n$($fail.Tee)" `
            -Severity Critical
    }
    elseif ($fail.Baidid -ge 1GB) {
        Send-AlertMessage `
            -Message "Suur fail: $($fail.Nimi) ($($fail.Suurus))`n$($fail.Tee)" `
            -Severity Warning
    }
}