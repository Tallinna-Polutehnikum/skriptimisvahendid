import argparse
import csv

parser = argparse.ArgumentParser(description="Filtreeri IT-seadmeid CSV-failist")
parser.add_argument("--osakond", help="Filtreeri osakonna järgi")
parser.add_argument("--tüüp",    help="Filtreeri tüübi järgi")
parser.add_argument("--väljund", help="Salvesta tulemus faili")
# Lisatud argument --os operatsioonisüsteemi järgi filtreerimiseks
parser.add_argument("--os", help="Filtreeri operatsioonisüsteemi järgi, nt: windows 11")
# Lisatud argument sorteerimiseks veeru nime järgi
parser.add_argument("--sorteeri", help="Sorteeri tulemus veeru järgi, nt: nimi või osakond")
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
# Filtreerimine operatsioonisüsteemi järgi
if args.os:
    tulemus = [s for s in tulemus if s["os"] == args.os]

# Sorteerimine veeru järgi
if args.sorteeri:
    tulemus = sorted(tulemus, key=lambda s: s[args.sorteeri])

# Kui kasutaja annab vale osakonna nime, kuvatakse : Leitud 0 seadet
# Kui filtrid andsid tühja tulemuse, kuva hoiatus
if len(tulemus) == 0:
    print("\nHoiatus: ühtegi seadet ei leitud. Kontrolli filtrite väärtusi.")

# kuva tulemus
print(f"\nLeitud {len(tulemus)} seadet:\n")
for seade in tulemus:
    print(f"  {seade['nimi']:<20} {seade['osakond']:<20} {seade['tüüp']}")

if args.väljund:
    with open(args.väljund, "w", newline="", encoding="utf-8") as f:
        kirjutaja = csv.DictWriter(f, fieldnames=seadmed[0].keys())
        kirjutaja.writeheader()
        kirjutaja.writerows(tulemus)
    print(f"\nTulemus salvestatud: {args.väljund}")
