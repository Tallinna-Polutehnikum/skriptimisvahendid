# Harjutus: kümme kõige suuremat faili

**Kursus:** KIT-24  
**Õpetaja:** Toivo Pärnpuu  
**Keel:** PowerShell

---

## Eesmärk

Kirjuta PowerShell skript, mis leiab kasutaja kodukaustas 10 kõige suuremat faili ja salvestab tulemuse CSV-faili. See on tüüpiline IT-administraatori ülesanne — enne kettaruumi täis saab, tahad teada, mis ruumi sööb.

---

## Tulemus

Skript loob faili `suurimad_failid.csv` sisuga:

```
Tee,Nimi,Suurus
C:\Users\toivo\Videos\backup.zip,backup.zip,2.3 GB
C:\Users\toivo\Downloads\installer.exe,installer.exe,847.2 MB
...
```

---

## Nõuded

- Otsing käib rekursiivselt läbi kõik alamkaustad
- Tulemuses on täpselt 10 faili, suurimast väikseimani
- Suurus kuvatakse sobivas ühikus (GB, MB või KB) — mitte baitides
- CSV-fail salvestatakse skriptiga samasse kausta

---

## Vihjenõuded

Ülesanne on jagatud viieks sammuks. Proovi iga samm ise lahendada — vihje avab alles siis, kui jooksed seina otsa.

---

### Samm 1 — leia kõik failid kodukaustas

**Mida vajad:** üks käsk, mis läbib kõik alamkaustad rekursiivselt.

<details>
<summary>Vihje</summary>

```powershell
Get-ChildItem -Path $HOME -Recurse -File -ErrorAction SilentlyContinue
```

`-Recurse` käib läbi kõik alamkaustad.  
`-File` tagastab ainult failid (mitte kaustad).  
`-ErrorAction SilentlyContinue` jätab vahele kaustad, millele pole ligipääsu.

</details>

---

### Samm 2 — sorteeri suuruse järgi ja võta 10 esimest

**Mida vajad:** torustik (`|`), sorteerimise käsk ja piiramise käsk.

<details>
<summary>Vihje</summary>

```powershell
... | Sort-Object -Property Length -Descending | Select-Object -First 10
```

`Length` on faili suurus baitides.  
`-Descending` sorteerib suurimast väikseimani.  
`Select-Object -First 10` võtab esimesed 10 rida.

</details>

---

### Samm 3 — teisenda baidid loetavasse ühikusse

**Mida vajad:** tingimuslause (`if`/`elseif`/`else`), jagamine ja ümardamine.

<details>
<summary>Vihje</summary>

```powershell
$baite = 1548234567

if ($baite -ge 1GB) {
    $suurus = "{0:N1} GB" -f ($baite / 1GB)
} elseif ($baite -ge 1MB) {
    $suurus = "{0:N1} MB" -f ($baite / 1MB)
} else {
    $suurus = "{0:N1} KB" -f ($baite / 1KB)
}
```

PowerShellis on `1GB`, `1MB`, `1KB` sisseehitatud konstandid.  
`"{0:N1}" -f arv` formaadib arvu ühe kümnendkohaga.

</details>

---

### Samm 4 — ehita iga faili kohta objekt

**Mida vajad:** `foreach` tsükkel ja kohandatud objekt (`[PSCustomObject]`).

<details>
<summary>Vihje</summary>

```powershell
$tulemus = foreach ($fail in $failid) {
    [PSCustomObject]@{
        Tee    = $fail.FullName
        Nimi   = $fail.Name
        Suurus = # ... sinu kood siit
    }
}
```

`$fail.FullName` — täielik tee koos failinimega  
`$fail.Name` — ainult failinimi  
`$fail.Length` — suurus baitides

</details>

---

### Samm 5 — salvesta CSV-faili

**Mida vajad:** üks käsk, mis kirjutab objektide nimekirja CSV-faili.

<details>
<summary>Vihje</summary>

```powershell
$tulemus | Export-Csv -Path "suurimad_failid.csv" -NoTypeInformation -Encoding UTF8
```

`-NoTypeInformation` jätab välja PowerShelli sisemise tüübirea CSV algusest.  
`-Encoding UTF8` tagab, et täpitähed salvestuvad õigesti.

</details>

---

## Tulemuse esitamine

Kopeeri valmis skript ja loodud CSV oma kausta ning tee PR:

```powershell
Copy-Item suurimad_failid.ps1  tulemused\Eesnimi_P\
Copy-Item suurimad_failid.csv  tulemused\Eesnimi_P\
```

```bash
git checkout -b harjutus-ps-Eesnimi
git add tulemused/Eesnimi_P/
git commit -m "Lisa PowerShell harjutus — Eesnimi P"
git push -u origin harjutus-ps-Eesnimi
```

Ava GitHubis **Compare & pull request** ja loo PR pealkirjaga:

```
PowerShell harjutus — Eesnimi P
```

---

## Lisaküsimused

1. Kuidas välistada skriptist teatud kaustu (nt `AppData`)? Uuri `-Exclude` parameetrit
2. Lisa CSV-sse veerg `Muudetud` — faili viimase muutmise kuupäev
3. Kuidas käivitada skripti nii, et otsingukoht antakse käsureal argumendina?