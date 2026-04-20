# Harjutus: käsurea argumendid Pythonis

**Kursus:** KIT-24  
**Õpetaja:** Toivo Pärnpuu  
**Moodul:** `argparse` (tuleb Pythoniga kaasa, pole vaja installida)

---

## Eesmärk

Eelmises harjutuses oli osakond ja filter koodis sees kirjutatud. Päriselu skriptid töötavad teisiti — filter antakse käsureal kaasa. Selles harjutuses teed eelmisest `seadmete_analyys.py` skriptist uue versiooni, mida saab paindlikult käivitada.

---

## Tulemus

Pärast harjutust töötab sinu skript nii:

```bash
# kuva kõik seadmed
python seadmed_filter.py

# filtreeri osakonna järgi
python seadmed_filter.py --osakond IT

# filtreeri seadme tüübi järgi
python seadmed_filter.py --tüüp laptop

# mõlemad korraga
python seadmed_filter.py --osakond Müük --tüüp laptop

# salvesta tulemus faili
python seadmed_filter.py --osakond IT --väljund it-seadmed.csv
```

---

## Ettevalmistus

Klooni repo ja liigu oma kausta:

```bash
git clone git@github.com:Tallinna-Polutehnikum/skriptimisvahendid.git
cd skriptimisvahendid
```

Kopeeri eelmise harjutuse `seadmed.csv` oma kausta või kasuta seda kohapeal. Loo uus fail `seadmed_filter.py`.

---

## Kood samm-sammult

### 1. osa — tutvumine argparse-ga

```python
import argparse

# loo parser ja kirjelda, mida skript teeb
parser = argparse.ArgumentParser(description="Filtreeri IT-seadmeid CSV-failist")

# lisa argumendid — kõik on valikulised (required=False on vaikimisi)
parser.add_argument("--osakond", help="Filtreeri osakonna järgi, nt: IT")
parser.add_argument("--tüüp",    help="Filtreeri tüübi järgi: laptop, desktop, server")
parser.add_argument("--väljund", help="Salvesta tulemus sellesse faili, nt: tulemus.csv")

# parsi argumendid — argumendid on nüüd args.osakond, args.tüüp, args.väljund
args = parser.parse_args()

# vaata, mida kasutaja andis
print(f"Osakond: {args.osakond}")
print(f"Tüüp:    {args.tüüp}")
print(f"Väljund: {args.väljund}")
```

Käivita erinevate argumentidega ja vaata, mis juhtub:

```bash
python seadmed_filter.py --osakond IT
python seadmed_filter.py --help
```

---

### 2. osa — loe CSV ja rakenda filter

```python
import argparse
import csv

parser = argparse.ArgumentParser(description="Filtreeri IT-seadmeid CSV-failist")
parser.add_argument("--osakond", help="Filtreeri osakonna järgi")
parser.add_argument("--tüüp",    help="Filtreeri tüübi järgi")
parser.add_argument("--väljund", help="Salvesta tulemus faili")
args = parser.parse_args()

# loe seadmed sisse
seadmed = []
with open("seadmed.csv", newline="", encoding="utf-8") as f:
    lugeja = csv.DictReader(f)
    for rida in lugeja:
        seadmed.append(rida)

# rakenda filtrid
tulemus = seadmed

if args.osakond:
    tulemus = [s for s in tulemus if s["osakond"] == args.osakond]

if args.tüüp:
    tulemus = [s for s in tulemus if s["tüüp"] == args.tüüp]

# kuva tulemus
print(f"Leitud {len(tulemus)} seadet:\n")
for seade in tulemus:
    print(f"  {seade['nimi']:<20} {seade['osakond']:<20} {seade['tüüp']}")
```

---

### 3. osa — salvesta tulemus faili

Lisa skripti lõppu:

```python
if args.väljund:
    with open(args.väljund, "w", newline="", encoding="utf-8") as f:
        kirjutaja = csv.DictWriter(f, fieldnames=seadmed[0].keys())
        kirjutaja.writeheader()
        kirjutaja.writerows(tulemus)
    print(f"\nTulemus salvestatud: {args.väljund}")
```

Testi:

```bash
python seadmed_filter.py --osakond IT --väljund it-seadmed.csv
```

---

## Mida sa õppisid

| Käsk | Tähendus |
|---|---|
| `argparse.ArgumentParser()` | loo argument-parser |
| `parser.add_argument("--nimi")` | lisa käsurea argument |
| `args = parser.parse_args()` | loe argumendid sisse |
| `args.osakond` | kasuta argumendi väärtust |
| `--help` | argparse genereerib abiinfo automaatselt |

---

## Lisaküsimused

1. Lisa argument `--os` — filtreeri operatsioonisüsteemi järgi (nt `Windows 10`)
2. Lisa argument `--sorteeri` — sorteeri tulemus veeru nime järgi
3. Mis juhtub, kui kasutaja annab vale osakonna nime? Kuidas näidata viisakat veateadet?

---

## Tulemuse esitamine

Kopeeri oma failid oma kausta ja tee PR.

```bash
cp seadmed_filter.py tulemused/Eesnimi_P/
cp it-seadmed.csv   tulemused/Eesnimi_P/   # kui lõid väljundfaili

git checkout -b harjutus-argparse-Eesnimi
git add tulemused/Eesnimi_P/
git commit -m "Lisa argparse harjutus — Eesnimi P"
git push -u origin harjutus-argparse-Eesnimi
```

Ava GitHubis **Compare & pull request** ja loo PR pealkirjaga:

```
Argparse harjutus — Eesnimi P
```