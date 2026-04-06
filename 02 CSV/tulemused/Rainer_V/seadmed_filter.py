import argparse
import csv

parser = argparse.ArgumentParser(description="Filtreeri IT-seadmeid CSV-failist")
parser.add_argument("--osakond", help="Filtreeri osakonna järgi")
parser.add_argument("--tüüp",    help="Filtreeri tüübi järgi")
parser.add_argument("--os",      help="Filtreeri operatsioonisüsteemi järgi")
parser.add_argument("--sorteeri", help="Sorteeri tulemused veeru järgi")
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

if args.os:
    tulemus = [s for s in tulemus if s["os"] == args.os]

def vota_sorteerimisvaartus(seade):
    return seade[args.sorteeri]

if args.sorteeri:
    if not seadmed:
        parser.error("CSV-failis pole andmeid, sorteerida ei saa.")
    if args.sorteeri not in seadmed[0]:
        voimalikud = ", ".join(seadmed[0].keys())
        parser.error(f"Tundmatu veerg sorteerimiseks: {args.sorteeri}. Võimalikud veerud: {voimalikud}")
    tulemus = sorted(tulemus, key=vota_sorteerimisvaartus)

# kuva tulemus
print(f"Leitud {len(tulemus)} seadet:\n")
for seade in tulemus:
    print(f"  {seade['nimi']:<20} {seade['osakond']:<20} {seade['tüüp']}")

if args.väljund:
    with open(args.väljund, "w", newline="", encoding="utf-8") as f:
        kirjutaja = csv.DictWriter(f, fieldnames=seadmed[0].keys())
        kirjutaja.writeheader()
        kirjutaja.writerows(tulemus)
    print(f"\nTulemus salvestatud: {args.väljund}")
