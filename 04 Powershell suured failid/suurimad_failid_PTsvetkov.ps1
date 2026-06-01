function Vorminda-Suurus {
    param (
        [long]$baite
    )

    if ($baite -ge 1GB) {
        return "{0:N1} GB" -f ($baite / 1GB)
    }
    elseif ($baite -ge 1MB) {
        return "{0:N1} MB" -f ($baite / 1MB)
    }
    else {
        return "{0:N1} KB" -f ($baite / 1KB)
    }
}

$failid = Get-ChildItem -Path $HOME -Recurse -File -ErrorAction SilentlyContinue |
    Sort-Object -Property Length -Descending |
    Select-Object -First 10

$tulemus = foreach ($fail in $failid) {
    [PSCustomObject]@{
        Tee    = $fail.FullName
        Nimi   = $fail.Name
        Suurus = Vorminda-Suurus $fail.Length
    }
}

$tulemus | Export-Csv -Path "suurimad_failid.csv" -NoTypeInformation -Encoding UTF8

Write-Host "10 kõige suuremat faili:"
$tulemus | Format-Table -AutoSize

Write-Host ""
Write-Host "Salvestatud: suurimad_failid.csv"