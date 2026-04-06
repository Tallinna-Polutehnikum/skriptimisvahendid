import argparse
import csv

parser = argparse.ArgumentParser(description="Filtreeri IT-seadmeid CSV-failist")
parser.add_argument("--osakond", help="Filtreeri osakonna järgi")
parser.add_argument("--tüüp",    help="Filtreeri tüübi järgi")
parser.add_argument("--väljund", help="Salvesta tulemus faili")
parser.add_argument("--os",      help="Filtreeri operatsioonisüsteemi järgi, nt: 'Windows 10'")
parser.add_argument("--sorteeri",help="Sorteeri veeru nime järgi, nt: nimi, osakond, tüüp")
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
    # kontrolli, kas osakond üldse eksisteerib
    olemasolevad_osakonnad = {s["osakond"] for s in seadmed}
    if args.osakond not in olemasolevad_osakonnad:
        print(f"Viga: osakonda '{args.osakond}' ei leitud.")
        print(f"Olemasolevad osakonnad: {', '.join(sorted(olemasolevad_osakonnad))}")
        exit(1)
    tulemus = [s for s in tulemus if s["osakond"] == args.osakond]

if args.tüüp:
    tulemus = [s for s in tulemus if s["tüüp"] == args.tüüp]

if args.os:
    tulemus = [s for s in tulemus if s["os"] == args.os]

if args.sorteeri:
    # kontrolli, kas veerg eksisteerib
    olemasolevad_veerud = seadmed[0].keys()
    if args.sorteeri not in olemasolevad_veerud:
        print(f"Viga: veergu '{args.sorteeri}' ei leitud.")
        print(f"Olemasolevad veerud: {', '.join(olemasolevad_veerud)}")
        exit(1)
    tulemus = sorted(tulemus, key=lambda s: s[args.sorteeri])

# kuva tulemus
print(f"Leitud {len(tulemus)} seadet:\n")
for seade in tulemus:
    print(f"  {seade['nimi']:<20} {seade['osakond']:<15} {seade['tüüp']:<10} {seade['os']}")

if args.väljund:
    with open(args.väljund, "w", newline="", encoding="utf-8") as f:
        kirjutaja = csv.DictWriter(f, fieldnames=seadmed[0].keys())
        kirjutaja.writeheader()
        kirjutaja.writerows(tulemus)
    print(f"\nTulemus salvestatud: {args.väljund}")