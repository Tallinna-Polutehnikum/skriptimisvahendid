import csv
from datetime import date
from datetime import timedelta

seadmed = []  # tühi nimekiri, kuhu salvestame kõik read

with open("it-seadmed.csv", newline="", encoding="utf-8") as f:
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


print("Aruanne salvestatud faili: probleemseadmed.csv")


# ainult W10 seadmed
win10_seadmed = [
    s for s in seadmed
    if s["os"].startswith("Windows 10")
]

print("\nWindows 10 seadmed (vajavad Windows 11 uuendust):")
for s in win10_seadmed:
    print(f"  {s['nimi']} — {s['os']}")

vähe_ruumi_sorteeritud = sorted(vähe_ruumi, key=lambda x: x[1])

print("\nSeadmed, kus vaba kettaruum alla 10% (sorteeritud):")
for nimi, protsent in vähe_ruumi_sorteeritud:
    print(f"  {nimi} — {protsent}% vaba")


kuue_kuu_parast = tana + timedelta(days=183)
garantii_varsti = []

for seade in seadmed:
    garantii = date.fromisoformat(seade["garantii_lõpp"])
    if tana <= garantii <= kuue_kuu_parast:
        garantii_varsti.append((seade["nimi"], seade["garantii_lõpp"]))

print(f"\nGarantiid lõpevad järgmise 6 kuu jooksul: {len(garantii_varsti)} seadet")
for nimi, kp in garantii_varsti:
    print(f"  {nimi} — lõppeb {kp}")

