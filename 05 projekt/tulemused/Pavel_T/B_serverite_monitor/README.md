# B - Serverite saadavuse monitor

## Käivitamine

PowerShellis:

./kontrolli-hostid.ps1

## Sõltuvused

- PowerShell 7

## Sisend

Skript loeb hostid failist `hostid.csv`.

## Väljund

Skript kontrollib hostide saadavust ja salvestab tulemuse CSV-faili.

Näide:

saadavus_2026-05-31.csv

## Valikud

Kasutasin `Test-Connection` käsku, sest minu PowerShell 7 Linux/WSL keskkonnas `Test-NetConnection` ei olnud saadaval.

Kui mõni host ei vasta, märgitakse see olekuga `FAIL`, kuid skript jätkab tööd.