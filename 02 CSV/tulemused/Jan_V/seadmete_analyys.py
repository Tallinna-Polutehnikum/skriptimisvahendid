import csv
from datetime import date, timedelta

seadmed = []

with open("seadmed.csv", newline="", encoding="utf-8") as f:
    lugeja = csv.DictReader(f)
    for rida in lugeja:
        seadmed.append(rida)

print(f"Kokku seadmeid andmebaasis: {len(seadmed)}")
print()

print("Näidis — esimene seade:")
print("-" * 40)
for väli, väärtus in seadmed[0].items():
    print(f"  {väli}: {väärtus}")

tana = date.today()

vanad_uuendused  = []
vähe_ruumi       = []
aegunud_garantii = []
win10_seadmed    = []

for seade in seadmed:

    uuendus = date.fromisoformat(seade["viimane_uuendus"])
    paevi_tagasi = (tana - uuendus).days
    if paevi_tagasi > 365:
        vanad_uuendused.append((seade["nimi"], paevi_tagasi))

    kokku = int(seade["kettaruum_gb"])
    vaba  = int(seade["kettaruum_vaba_gb"])
    protsent = vaba / kokku * 100
    if protsent < 10:
        vähe_ruumi.append((seade["nimi"], round(protsent, 1)))

    garantii = date.fromisoformat(seade["garantii_lõpp"])
    if garantii < tana:
        aegunud_garantii.append((seade["nimi"], seade["garantii_lõpp"]))

    if seade["os"] == "Windows 10":
        win10_seadmed.append(seade["nimi"])

print("Seadmed, mida pole üle aasta uuendatud:")
for nimi, paevi in vanad_uuendused:
    print(f"  {nimi} — {paevi} päeva tagasi")

vähe_ruumi_sorditud = sorted(vähe_ruumi, key=lambda x: x[1])

print("\nSeadmed, kus vaba kettaruum alla 10% (sorditult):")
for nimi, protsent in vähe_ruumi_sorditud:
    print(f"  {nimi} — {protsent}% vaba")

print("\nSeadmed, mille garantii on lõppenud:")
for nimi, kuupäev in aegunud_garantii:
    print(f"  {nimi} — lõppes {kuupäev}")

kuue_kuu_parast = tana + timedelta(days=183)
garantii_lõpeb_peatselt = [
    seade for seade in seadmed
    if tana <= date.fromisoformat(seade["garantii_lõpp"]) <= kuue_kuu_parast
]

print(f"\nSeadmed, mille garantii lõpeb järgmise 6 kuu jooksul ({kuue_kuu_parast}):")
for seade in garantii_lõpeb_peatselt:
    print(f"  {seade['nimi']} — lõpeb {seade['garantii_lõpp']}")
print(f"  Kokku: {len(garantii_lõpeb_peatselt)} seadet")

print(f"\nWindows 10 seadmed (soovitav uuendada Windows 11-le): {len(win10_seadmed)} tk")
for nimi in win10_seadmed:
    print(f"  {nimi}")

osakonnad = {}

for seade in seadmed:
    osakond = seade["osakond"]
    if osakond not in osakonnad:
        osakonnad[osakond] = 0
    osakonnad[osakond] += 1

print("\nSeadmete arv osakondade kaupa:")
for osakond, arv in sorted(osakonnad.items()):
    print(f"  {osakond}: {arv} seadet")

vaba_ruumid = [int(s["kettaruum_vaba_gb"]) for s in seadmed]
keskmine_vaba = sum(vaba_ruumid) / len(vaba_ruumid)
print(f"\nKeskmine vaba kettaruum: {round(keskmine_vaba, 1)} GB")


with open("probleemseadmed.csv", "w", newline="", encoding="utf-8") as f:
    väljad = ["nimi", "probleem", "detail"]
    kirjutaja = csv.DictWriter(f, fieldnames=väljad)
    kirjutaja.writeheader()

    for nimi, paevi in vanad_uuendused:
        kirjutaja.writerow({
            "nimi": nimi,
            "probleem": "vana uuendus",
            "detail": f"{paevi} päeva tagasi"
        })

    for nimi, protsent in vähe_ruumi_sorditud:
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

    for seade in garantii_lõpeb_peatselt:
        kirjutaja.writerow({
            "nimi": seade["nimi"],
            "probleem": "garantii lõpeb peatselt",
            "detail": seade["garantii_lõpp"]
        })

    for nimi in win10_seadmed:
        kirjutaja.writerow({
            "nimi": nimi,
            "probleem": "Windows 10 — vajab uuendust",
            "detail": "Uuenda Windows 11-le"
        })

print("Aruanne salvestatud faili: probleemseadmed.csv")