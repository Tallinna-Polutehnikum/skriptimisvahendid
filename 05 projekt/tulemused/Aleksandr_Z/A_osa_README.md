# Logianalüüsi skript (Ülesanne A)

## Kirjeldus

See skript analüüsib teavituste logifaili (`ps-alerts.log`) ja koostab kokkuvõtte:

* mitu teadet kokku
* jaotus raskusastmete järgi (Info, Warning, Critical)
* ebaõnnestunud teated (FAIL)
* top allikad (millised seadmed saadavad enim teateid)
* statistika päevade lõikes

Lisaks salvestatakse tulemused CSV-faili.

---

## ▶Käivitamine

```bash
python analyysi_logi.py
```

Või oma failiga:

```bash
python analyysi_logi.py minu_logi.log
```

CSV väljundi nime muutmine:

```bash
python analyysi_logi.py ps-alerts.log --valjund tulemus.csv
```

---

## Sisendfail

Vaikimisi loeb skript faili:

```
ps-alerts.log
```

Logi formaat:

```
YYYY-MM-DD HH:MM:SS    [OK/FAIL]    Severity    Source    Message    (optional Error)
```

Näide:

```
2026-04-15 02:33:11    [FAIL]    Critical    DC01    Teenus maas    Timeout
```

---

## Väljund

### 1. Konsool

Kuvatakse kokkuvõte:

* periood
* teadete arv
* raskusastmed
* top allikad
* ASCII graafik (Critical teated)

### 2. CSV fail

Fail:

```
analyys_paevad.csv
```

Näide:

```
Paev,Kokku,Info,Warning,Critical,Fail
2026-04-14,3,1,1,1,0
...
```

---

## Kasutatud tehnoloogiad

* Python 3
* moodulid:

  * argparse
  * pathlib
  * datetime
  * collections
  * csv

---

## Märkused

* Logifail peab kasutama TAB eraldajat
* Vigased read jäetakse vahele (skript ei katke)
* Tühi logifail ei põhjusta viga

---

## Disainiotsused

* Kasutatud `defaultdict` ja `Counter`, et lihtsustada loendamist
* Kuupäevad parsitakse `datetime`-ga (mitte stringidena)
* CSV väljund valitud lihtsaks edasiseks töötlemiseks (Excel jne)
* ASCII graafik tehtud lihtsal kujul (`██`)

---
