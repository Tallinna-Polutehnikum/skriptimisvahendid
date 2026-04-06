import csv
from datetime import date, timedelta

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

# Probleemide otsimine seadmete seas
tana = date.today()

vanad_uuendused  = []  # seadmed, mida pole üle aasta uuendatud
vähe_ruumi       = []  # seadmed, kus vaba kettaruum alla 10%
aegunud_garantii = []  # seadmed, mille garantii on lõppenud
aegumas_garantii = []  # seadmed, mille garantii lõpuni on vähem kui 6 kuud
aegunud_os       = []  # seadmed, millel on Windows 10

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
    elif garantii < tana + timedelta(days=180):
        aegumas_garantii.append((seade["nimi"], seade["garantii_lõpp"]))

    # Kontrolli, kas OS on Windows 10
    if seade["os"] == "Windows 10":
        aegunud_os.append((seade["nimi"], seade["os"]))

def vota_vaba_ruumi_protsent(kirje):
    nimi, protsent = kirje
    return protsent

print("Seadmed, mida pole üle aasta uuendatud:")
for nimi, paevi in vanad_uuendused:
    print(f"  {nimi} — {paevi} päeva tagasi")

print("\nSeadmed, kus vaba kettaruum alla 10%:")
for nimi, protsent in sorted(vähe_ruumi, key=vota_vaba_ruumi_protsent):
    print(f"  {nimi} — {protsent}% vaba")

print("\nSeadmed, mille garantii on lõppenud:")
for nimi, kuupäev in aegunud_garantii:
    print(f"  {nimi} — lõppes {kuupäev}")

print("\nSeadmed, mille garantii on lõppemas:")
for nimi, kuupäev in aegumas_garantii:
    print(f"  {nimi} — lõpeb {kuupäev}")

print("\nSeadmed, millel on Windows 10 ja vajavad uuendamist:")
for nimi, os in aegunud_os:
    print(f"  {nimi}")

# Arvutused osakondade kaupa
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

# Kirjuta andmed uude aruande faili
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

    for nimi, kuupäev in aegumas_garantii:
        kirjutaja.writerow({
            "nimi": nimi,
            "probleem": "garantii lõppemas",
            "detail": kuupäev
        })

    for nimi, os in aegunud_os:
        kirjutaja.writerow({
            "nimi": nimi,
            "probleem": "aegunud os",
            "detail": os
        })

print("Aruanne salvestatud faili: probleemseadmed.csv")
