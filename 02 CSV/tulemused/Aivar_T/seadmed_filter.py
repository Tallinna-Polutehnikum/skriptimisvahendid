import argparse
import csv

parser = argparse.ArgumentParser(description="Filtreeri IT-seadmeid CSV-failist")
parser.add_argument("--osakond", help="Filtreeri osakonna järgi")
parser.add_argument("--tüüp", help="Filtreeri tüübi järgi")
parser.add_argument("--väljund", help="Salvesta tulemus faili")
args = parser.parse_args()

seadmed = []
with open("seadmed.csv", newline="", encoding="utf-8") as f:
    lugeja = csv.DictReader(f)
    for rida in lugeja:
        seadmed.append(rida)

tulemus = seadmed

if args.osakond:
    tulemus = [s for s in tulemus if s["osakond"] == args.osakond]

if args.tüüp:
    tulemus = [s for s in tulemus if s["tüüp"] == args.tüüp]

print(f"Leitud {len(tulemus)} seadet:\n")
for seade in tulemus:
    print(f"  {seade['nimi']:<20} {seade['osakond']:<20} {seade['tüüp']}")


if args.väljund:
    with open(args.väljund, "w", newline="", encoding="utf-8") as f:
        kirjutaja = csv.DictWriter(f, fieldnames=seadmed[0].keys())
        kirjutaja.writeheader()
        kirjutaja.writerows(tulemus)
    print(f"\nTulemus salvestatud: {args.väljund}")