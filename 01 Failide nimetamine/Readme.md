# Harjutus: failide automaatne ümbernimetamine

**Kursus:** KIT-24  
**Õpetaja:** Toivo Pärnpuu  
**Moodul:** `os` (tuleb Pythoniga kaasa, pole vaja installida)

---

## Eesmärk

Õpid, kuidas Python saab failisüsteemiga suhelda — loed kaustas olevaid faile, muudad nende nimesid ja kasutad tsüklit korraga mitme faili töötlemiseks.

---

## Ettevalmistus

1. Klooni see repositoorium oma arvutisse:

```bash
git clone git@github.com:Tallinna-Polutehnikum/skriptimisvahendid.git
cd skriptimisvahendid
```

2. Ava kaust `failid-harjutus` — seal on 10 segase nimega faili, millega harjutad.

3. Loo uus fail nimega `umbernimetamine.py` samasse kausta, kuhu on alla laaditud `failid-harjutus`.

---

## Kood samm-sammult

### 1. osa — vaata, mis failid kaustas on

```python
import os  # os-moodul võimaldab failide ja kaustadega töötada

kaust = "failid-harjutus"  # kaust, milles tegutseme

print("Failid enne ümbernimetamist:")
print("-" * 35)

failid = os.listdir(kaust)   # tagastab nimekirja kaustas olevatest failidest
for failinimi in failid:
    print(failinimi)
```

Käivita skript ja vaata tulemust. Peaksid nägema 10 faili segaste nimedega.

---

### 2. osa — nimeta tühikud allkriipsudeks

Tühikutega failinimed põhjustavad sageli probleeme terminalis ja skriptides. Asendame need allkriipsuga `_`.

```python
print("Nimetan tühikud allkriipsudeks...")
print("-" * 35)

for failinimi in os.listdir(kaust):

    if " " in failinimi:  # kontrolli, kas failinimi sisaldab tühikut

        uus_nimi = failinimi.replace(" ", "_")  # asenda kõik tühikud

        vana_tee = os.path.join(kaust, failinimi)  # täielik tee vanale failile
        uus_tee  = os.path.join(kaust, uus_nimi)   # täielik tee uuele failile

        os.rename(vana_tee, uus_tee)  # teeb ümbernimetamise

        print(f"  {failinimi}  →  {uus_nimi}")
```

---

### 3. osa — lisa eesliide failitüübi järgi

Pildifailidele (`.jpg`) lisame eesliite `pilt_`, tekstifailidele (`.txt`) eesliite `tekst_`.

```python
print("Lisan eesliited failitüübi järgi...")
print("-" * 35)

for failinimi in os.listdir(kaust):

    if failinimi.endswith(".jpg") and not failinimi.startswith("pilt_"):
        uus_nimi = "pilt_" + failinimi

    elif failinimi.endswith(".txt") and not failinimi.startswith("tekst_"):
        uus_nimi = "tekst_" + failinimi

    else:
        continue  # see fail ei vaja muutmist, jätame vahele

    vana_tee = os.path.join(kaust, failinimi)
    uus_tee  = os.path.join(kaust, uus_nimi)
    os.rename(vana_tee, uus_tee)
    print(f"  {failinimi}  →  {uus_nimi}")
```

---

### 4. osa — lõpptulemus

```python
print("Failid pärast ümbernimetamist:")
print("-" * 35)
for failinimi in sorted(os.listdir(kaust)):
    print(failinimi)
```

Kui kõik läks õigesti, peaksid nägema failinimesid kujul:

```
pilt_foto_puhkus_1.jpg
pilt_kass.jpg
tekst_aruanne_aprill.txt
tekst_dokument_vana.txt
...
```

---

## Mida sa õppisid

| Käsk | Tähendus |
|---|---|
| `os.listdir(kaust)` | loe kaustas olevad failid |
| `os.rename(vana, uus)` | nimeta fail ümber |
| `os.path.join(kaust, fail)` | ehita failitee kokku |
| `str.replace(a, b)` | asenda tekstis tähemärke |
| `str.endswith(".jpg")` | kontrolli faililaiend |
| `str.startswith("pilt_")` | kontrolli nime algust |

---

## Lisaküsimused

1. Muuda kõik failinimed väiketähtedeks — uuri meetodit `.lower()`
2. Lisa failinimede ette tänane kuupäev — uuri moodulit `datetime`
3. Mis juhtub, kui käivitad skripti teist korda? Kuidas seda vältida?

---

## Tulemuse esitamine — Pull Request

Kui harjutus on tehtud, esita oma tulemus Pull Requesti kaudu.

### 1. Fork ja klooni repo

Mine [github.com/Tallinna-Polutehnikum/skriptimisvahendid](https://github.com/Tallinna-Polutehnikum/skriptimisvahendid), tee **Fork** ja klooni see oma arvutisse.

### 2. Loo oma kaust

Loo repo sees kaust `tulemused/EESNIMI_P` (asenda oma eesnime ja perekonnanime esitähega):

```bash
mkdir -p tulemused/Marko_T
```

### 3. Kopeeri oma skript sinna

```bash
cp umbernimetamine.py tulemused/Marko_T/
```

### 4. Commit ja push

```bash
git checkout -b harjutus-failid-EESNIMI
git add tulemused/
git commit -m "Lisa failide ümbernimetamise harjutus — Eesnimi P"
git push -u origin harjutus-failid-EESNIMI
```

### 5. Ava Pull Request

Mine GitHubis oma fork'i lehele, klõpsa **Compare & pull request** ja loo PR pealkirjaga:

```
Failide ümbernimetamine — Eesnimi P
```

---

*Kui jooksed probleemi otsa, ava repositooriumis **Issue** ja kirjelda, mis juhtus.*