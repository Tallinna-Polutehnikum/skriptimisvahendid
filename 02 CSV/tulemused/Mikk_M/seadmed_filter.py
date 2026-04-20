# 1. osa — tutvumine argparse-ga
import argparse

# loo parser ja kirjelda, mida skript teeb
parser = argparse.ArgumentParser(description="Filtreeri IT-seadmeid CSV-failist")

# lisa argumendid — kõik on valikulised (required=False on vaikimisi)
parser.add_argument("--osakond", help="Filtreeri osakonna järgi, nt: IT")
parser.add_argument("--tüüp",    help="Filtreeri tüübi järgi: laptop, desktop, server")
parser.add_argument("--operatsioonisusteem", help="Filtreeri operatsioonisüsteemi järgi, nt: Windows 10")
parser.add_argument("--sorteeri", help="Sorteeri tulemuse veeru järgi, nt: nimi, osakond, tüüp")
parser.add_argument("--väljund", help="Salvesta tulemus sellesse faili, nt: tulemus.csv")

# parsi argumendid — argumendid on nüüd args.osakond, args.tüüp, args.väljund
args = parser.parse_args()

# vaata, mida kasutaja andis
print(f"Osakond: {args.osakond}")
print(f"Tüüp:    {args.tüüp}")
print(f"Väljund: {args.väljund}")

# 2. osa — loe CSV ja rakenda filter
import argparse
import csv

parser = argparse.ArgumentParser(description="Filtreeri IT-seadmeid CSV-failist")
parser.add_argument("--osakond", help="Filtreeri osakonna järgi")
parser.add_argument("--tüüp",    help="Filtreeri tüübi järgi")
parser.add_argument("--operatsioonisusteem", help="Filtreeri operatsioonisüsteemi järgi, nt: Windows 10")
parser.add_argument("--sorteeri", help="Sorteeri tulemuse veeru järgi, nt: nimi, osakond, tüüp")
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

if args.operatsioonisusteem:
    tulemus = [s for s in tulemus if s["os"] == args.operatsioonisusteem]

if args.sorteeri:
    veerg = args.sorteeri
    if veerg in seadmed[0]:
        tulemus = sorted(tulemus, key=lambda s: s[veerg])

# kuva tulemus
print(f"Leitud {len(tulemus)} seadet:\n")
for seade in tulemus:
    print(f"  {seade['nimi']:<20} {seade['osakond']:<20} {seade['tüüp']}")

# 3. osa — salvesta tulemus faili
if args.väljund:
    with open(args.väljund, "w", newline="", encoding="utf-8") as f:
        kirjutaja = csv.DictWriter(f, fieldnames=seadmed[0].keys())
        kirjutaja.writeheader()
        kirjutaja.writerows(tulemus)
    print(f"\nTulemus salvestatud: {args.väljund}")
