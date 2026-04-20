param(
    [Parameter(Position = 0)]
    [string]$Otsingukoht = $HOME,

    [string[]]$ValistaKaustad = @("AppData")
)

if (-not (Test-Path -Path $Otsingukoht -PathType Container)) {
    Write-Error "Otsingukoht ei ole olemas või ei ole kaust: $Otsingukoht"
    exit 1
}

$valistaRegex = if ($ValistaKaustad.Count -gt 0) {
    '(\\|/)(?:' + (($ValistaKaustad | ForEach-Object { [Regex]::Escape($_) }) -join '|') + ')(\\|/)'
}
else {
    $null
}

$failid = Get-ChildItem -Path $Otsingukoht -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { -not $valistaRegex -or $_.FullName -notmatch $valistaRegex } |
    Sort-Object -Property Length -Descending |
    Select-Object -First 10

$tulemus = foreach ($fail in $failid) {
    if ($fail.Length -ge 1GB) {
        $suurus = "{0:N1} GB" -f ($fail.Length / 1GB)
    }
    elseif ($fail.Length -ge 1MB) {
        $suurus = "{0:N1} MB" -f ($fail.Length / 1MB)
    }
    else {
        $suurus = "{0:N1} KB" -f ($fail.Length / 1KB)
    }

    [PSCustomObject]@{
        Tee      = $fail.FullName
        Nimi     = $fail.Name
        Suurus   = $suurus
        Muudetud = $fail.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
    }
}

$skriptiKaust = Split-Path -Parent $MyInvocation.MyCommand.Path
$csvFail = Join-Path -Path $skriptiKaust -ChildPath "suurimad_failid.csv"

$tulemus | Export-Csv -Path $csvFail -NoTypeInformation -Encoding UTF8

Write-Host "Tulemus salvestatud: $csvFail"
