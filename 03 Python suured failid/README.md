# Harjutus: kümme kõige suuremat faili

**Kursus:** KIT-24  
**Õpetaja:** Toivo Pärnpuu  
**Moodul:** `pathlib`, `csv` (tulevad Pythoniga kaasa)

---

## Eesmärk

Kirjuta Python skript, mis leiab kasutaja kodukaustas 10 kõige suuremat faili ja salvestab tulemuse CSV-faili. See on tüüpiline IT-administraatori ülesanne — enne kettaruumi täis saab, tahad teada, mis ruumi sööb.

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
- CSV-fail salvestatakse kausta `tulemused\Eesnimi_P\`

---

## Algoritm

Enne kodeerimist — mida skript peab tegema, samm-sammult:

1. Määra otsingukoht — kasutaja kodukaust
2. Liigu rekursiivselt läbi kõik alamkaustad
3. Kogu kokku kõik failid (kaustad jäta vahele)
4. Kui mõnele failile pole ligipääsu, jäta see vahele ja jätka
5. Sorteeri failid suuruse järgi — suurim esimesena
6. Võta nimekirjast 10 esimest
7. Iga faili kohta:
   - salvesta täielik tee
   - salvesta failinimi
   - teisenda suurus baitidest loetavasse ühikusse (GB / MB / KB)
8. Loo väljundkaust kui seda pole olemas
9. Kirjuta tulemus CSV-faili koos päisereaga

---

## Vihjenõuded

Ülesanne on jagatud viieks sammuks. Proovi iga samm ise lahendada — vihje avab alles siis, kui jooksed seina otsa.

---

### Samm 1 — leia kõik failid kodukaustas

**Mida vajad:** `pathlib` moodul ja meetod, mis läbib kõik alamkaustad rekursiivselt.

<details>
<summary>Vihje</summary>

```python
from pathlib import Path

kodu = Path.home()  # kasutaja kodukaust (~)

failid = []
for fail in kodu.rglob("*"):        # rglob käib läbi kõik alamkaustad
    if fail.is_file():              # jäta kaustad välja
        failid.append(fail)
```

`Path.home()` tagastab kodukaustatee (`C:\Users\kasutajanimi` Windowsis).  
`rglob("*")` leiab kõik failid ja kaustad rekursiivselt.  
`fail.is_file()` kontrollib, et tegu on failiga, mitte kaustaga.

Mõned kaustad võivad anda `PermissionError` — sellest järgmises sammus.

</details>

---

### Samm 2 — sorteeri suuruse järgi ja võta 10 esimest

**Mida vajad:** `sorted()` funktsioon `key=` argumendiga, lõikamine `[:10]` ja vigade käsitlemine.

<details>
<summary>Vihje</summary>

```python
failid_sorditud = sorted(
    failid,
    key=lambda f: f.stat().st_size,   # sorteeri faili suuruse järgi
    reverse=True                       # suurimast väikseimani
)[:10]                                 # võta 10 esimest
```

`f.stat().st_size` tagastab faili suuruse baitides.  
`lambda f: ...` on lühike funktsioon sorteerimiseks.  
Kui mõnele failile pole ligipääsu, tekib `PermissionError` — kasuta `try/except`:

```python
failid = []
for fail in kodu.rglob("*"):
    try:
        if fail.is_file():
            failid.append(fail)
    except PermissionError:
        continue   # jäta vahele ja liigu edasi
```

</details>

---

### Samm 3 — teisenda baidid loetavasse ühikusse

**Mida vajad:** tingimuslause `if/elif/else` ja jagamine.

<details>
<summary>Vihje</summary>

```python
def vorminda_suurus(baidid):
    if baidid >= 1_073_741_824:          # 1 GB = 1024³ baiti
        return f"{baidid / 1_073_741_824:.1f} GB"
    elif baidid >= 1_048_576:            # 1 MB = 1024² baiti
        return f"{baidid / 1_048_576:.1f} MB"
    else:                                # KB
        return f"{baidid / 1024:.1f} KB"
```

`:.1f` formaadib arvu ühe kümnendkohaga.  
`1_073_741_824` — Pythonis saab arvu loetavamaks teha allkriipsudega.

</details>

---

### Samm 4 — ehita iga faili kohta sõnastik

**Mida vajad:** `for` tsükkel ja sõnastik (`dict`) iga faili andmetega.

<details>
<summary>Vihje</summary>

```python
tulemus = []

for fail in failid_sorditud:
    suurus = fail.stat().st_size
    tulemus.append({
        "Tee":    str(fail),          # täielik tee koos failinimega
        "Nimi":   fail.name,          # ainult failinimi
        "Suurus": vorminda_suurus(suurus)
    })
```

`str(fail)` teisendab `Path`-objekti tekstiks.  
`fail.name` tagastab ainult failinime ilma teeta.

</details>

---

### Samm 5 — salvesta CSV-faili

**Mida vajad:** `csv.DictWriter` ja `Path` kausta loomiseks.

<details>
<summary>Vihje</summary>

```python
import csv

väljund = Path("tulemused/Eesnimi_P/suurimad_failid.csv")
väljund.parent.mkdir(parents=True, exist_ok=True)  # loo kaust kui pole olemas

with open(väljund, "w", newline="", encoding="utf-8") as f:
    kirjutaja = csv.DictWriter(f, fieldnames=["Tee", "Nimi", "Suurus"])
    kirjutaja.writeheader()
    kirjutaja.writerows(tulemus)

print(f"Salvestatud: {väljund}")
```

`parents=True` loob vajadusel ka vahekaustad.  
`exist_ok=True` ei anna viga, kui kaust juba olemas on.

</details>

---

## Mida sa õppisid

| Käsk | Tähendus |
|---|---|
| `Path.home()` | kasutaja kodukaust |
| `Path.rglob("*")` | rekursiivne faililoend |
| `fail.is_file()` | kontrolli, kas tegu on failiga |
| `fail.stat().st_size` | faili suurus baitides |
| `sorted(nimekiri, key=..., reverse=True)` | sorteerimine |
| `[:10]` | võta esimesed 10 elementi |
| `fail.name` | ainult failinimi |
| `Path.mkdir(parents=True, exist_ok=True)` | loo kaust |

---

## Lisaküsimused

1. Kuidas välistada skriptist kaust `AppData`? Uuri, kuidas kontrollida `fail.parts` sisu
2. Lisa CSV-sse veerg `Muudetud` — faili viimase muutmise kuupäev (`fail.stat().st_mtime`)
3. Kuidas anda otsingukoht käsureal argumendina? Uuri eelmist `argparse` harjutust

---

## Tulemuse esitamine

Nimeta oma skriptifail `suurimad_failid.py`. Skript salvestab CSV automaatselt õigesse kohta:

```
03 Python suured failid\
├── tulemused\
│   └── Eesnimi_P\
│       ├── suurimad_failid.py
│       └── suurimad_failid.csv
```

```bash
git checkout -b harjutus-suured-failid-Eesnimi
git add "03 Python suured failid/tulemused/Eesnimi_P/"
git commit -m "Lisa suurimad failid harjutus — Eesnimi P"
git push -u origin harjutus-suured-failid-Eesnimi
```

Ava GitHubis **Compare & pull request** ja loo PR pealkirjaga:

```
Suurimad failid — Eesnimi P
```