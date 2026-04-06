# 1. osa — loe CSV fail sisse
import csv
from datetime import date

seadmed = []  # tühi nimekiri, kuhu salvestame kõik read

with open("seadmed.csv", newline="", encoding="utf-8") as f:
    lugeja = csv.DictReader(f)  # DictReader loeb iga rea sõnastikuna
    for rida in lugeja:
        seadmed.append(rida)    # lisa iga seade nimekirja

print(f"Kokku seadmeid andmebaasis: {len(seadmed)}")
print()

# Vaata, milline näeb välja üks rida
print("Näidis — esimene seade:")
print("-" * 40)
for väli, väärtus in seadmed[0].items():
    print(f"  {väli}: {väärtus}")

# 2. osa — filtreerimine: leia probleemid
tana = date.today()

vanad_uuendused  = []  # seadmed, mida pole üle aasta uuendatud
vähe_ruumi       = []  # seadmed, kus vaba kettaruum alla 10%
aegunud_garantii = []  # seadmed, mille garantii on lõppenud

for seade in seadmed:

    # Kontrolli viimast uuendust
    uuendus = date.fromisoformat(seade["viimane_uuendus"])
    paevi_tagasi = (tana - uuendus).days
    if paevi_tagasi > 365:
        vanad_uuendused.append((seade["nimi"], paevi_tagasi))

    # Kontrolli kettaruumi
    kokku = int(seade["kettaruum_gb"])
    vaba  = int(seade["kettaruum_vaba_gb"])
    protsent = vaba / kokku * 100
    if protsent < 10:
        vähe_ruumi.append((seade["nimi"], round(protsent, 1)))

    # Kontrolli garantiid
    garantii = date.fromisoformat(seade["garantii_lõpp"])
    if garantii < tana:
        aegunud_garantii.append((seade["nimi"], seade["garantii_lõpp"]))

print("Seadmed, mida pole üle aasta uuendatud:")
for nimi, paevi in vanad_uuendused:
    print(f"  {nimi} — {paevi} päeva tagasi")

print("\nSeadmed, kus vaba kettaruum alla 10%:")
for nimi, protsent in vähe_ruumi:
    print(f"  {nimi} — {protsent}% vaba")

print("\nSeadmed, mille garantii on lõppenud:")
for nimi, kuupäev in aegunud_garantii:
    print(f"  {nimi} — lõppes {kuupäev}")

# 3. osa — arvutused osakondade kaupa
osakonnad = {}  # sõnastik: osakonna nimi → seadmete arv

for seade in seadmed:
    osakond = seade["osakond"]
    if osakond not in osakonnad:
        osakonnad[osakond] = 0
    osakonnad[osakond] += 1

print("\nSeadmete arv osakondade kaupa:")
for osakond, arv in sorted(osakonnad.items()):
    print(f"  {osakond}: {arv} seadet")

# Keskmine vaba kettaruum
vaba_ruumid = [int(s["kettaruum_vaba_gb"]) for s in seadmed]
keskmine_vaba = sum(vaba_ruumid) / len(vaba_ruumid)
print(f"\nKeskmine vaba kettaruum: {round(keskmine_vaba, 1)} GB")

# Windows 10 seadmete filter
print("\nWindows 10 seadmed (vajavad uuendust Windows 11-le):")

win10_seadmed = []

for seade in seadmed:
    if seade["os"] == "Windows 10":
        win10_seadmed.append(seade["nimi"])

for nimi in win10_seadmed:
    print(f"  {nimi}")

print(f"Kokku Windows 10 seadmeid: {len(win10_seadmed)}")

# Garantii lõpeb järgmise 6 kuu jooksul
from datetime import timedelta
garantii_varsti_loppemas = []

kuue_kuu_parast = tana + timedelta(days=182)

for seade in seadmed:
    garantii = date.fromisoformat(seade["garantii_lõpp"])

    if tana <= garantii <= kuue_kuu_parast:
        garantii_varsti_loppemas.append(
            (seade["nimi"], seade["garantii_lõpp"])
        )

print("\nSeadmed, mille garantii lõpeb järgmise 6 kuu jooksul:")

for nimi, kuup in garantii_varsti_loppemas:
    print(f"  {nimi} — lõpeb {kuup}")

print(f"Kokku: {len(garantii_varsti_loppemas)} seadet")

# 4. osa — kirjuta aruanne uude CSV-faili
with open("probleemseadmed.csv", "w", newline="", encoding="utf-8") as f:
    väljad = ["nimi", "probleem", "detail"]
    kirjutaja = csv.DictWriter(f, fieldnames=väljad)
    kirjutaja.writeheader()  # kirjuta päiserida

    for nimi, paevi in vanad_uuendused:
        kirjutaja.writerow({
            "nimi": nimi,
            "probleem": "vana uuendus",
            "detail": f"{paevi} päeva tagasi"
        })

    for nimi, protsent in vähe_ruumi:
        kirjutaja.writerow({
            "nimi": nimi,
            "probleem": "vähe kettaruumi",
            "detail": f"{protsent}% vaba"
        })

    for nimi, kuupäev in aegunud_garantii:
        kirjutaja.writerow({
            "nimi": nimi,
            "probleem": "garantii lõppenud",
            "detail": kuupäev
        })

    for nimi, kuup in garantii_varsti_loppemas:
        kirjutaja.writerow({
        "nimi": nimi,
        "probleem": "garantii lõpeb varsti",
        "detail": kuup  
        }) 
    
    for nimi in win10_seadmed:
        kirjutaja.writerow({
        "nimi": nimi,
        "probleem": "Windows 10",
        "detail": "vajab uuendust Windows 11-le"
    })

print("Aruanne salvestatud faili: probleemseadmed.csv")