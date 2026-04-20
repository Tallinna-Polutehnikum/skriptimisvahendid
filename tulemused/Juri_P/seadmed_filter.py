import argparse
import csv

# --- ARGUMENTS ---
parser = argparse.ArgumentParser(description="Filtreeri IT-seadmeid CSV-failist")

parser.add_argument("--osakond", help="Filtreeri osakonna järgi")
parser.add_argument("--tüüp", help="Filtreeri tüübi järgi")
parser.add_argument("--os", help="Filtreeri operatsioonisüsteemi järgi (nt Windows 10)")
parser.add_argument("--sorteeri", help="Sorteeri veeru järgi (nt nimi, osakond, tüüp, os)")
parser.add_argument("--väljund", help="Salvesta tulemus CSV-faili")

args = parser.parse_args()


seadmed = []
with open("seadmed.csv", newline="", encoding="utf-8") as f:
    lugeja = csv.DictReader(f)
    for rida in lugeja:
        seadmed.append(rida)

if not seadmed:
    print("Viga: CSV fail on tühi või puudub.")
    exit()

tulemus = seadmed


if args.osakond:
    olemas = {s["osakond"] for s in seadmed}
    if args.osakond not in olemas:
        print(f"Viga: osakonda '{args.osakond}' ei leitud.")
        print("Saadaolevad osakonnad:", ", ".join(sorted(olemas)))
        exit()

# --- FILTRID ---
if args.osakond:
    tulemus = [s for s in tulemus if s["osakond"] == args.osakond]

if args.tüüp:
    tulemus = [s for s in tulemus if s["tüüp"] == args.tüüp]

if args.os:
    tulemus = [s for s in tulemus if s["os"] == args.os]

# --- SORTEERIMINE ---
if args.sorteeri:
    try:
        tulemus = sorted(tulemus, key=lambda x: x[args.sorteeri])
    except KeyError:
        print(f"Viga: tundmatu veerg '{args.sorteeri}'")
        print("Võimalikud veerud:", ", ".join(seadmed[0].keys()))
        exit()


print(f"\nLeitud {len(tulemus)} seadet:\n")

for seade in tulemus:
    print(
        f"  {seade['nimi']:<20} "
        f"{seade['osakond']:<15} "
        f"{seade['tüüp']:<10} "
        f"{seade['os']}"
    )


if args.väljund:
    with open(args.väljund, "w", newline="", encoding="utf-8") as f:
        kirjutaja = csv.DictWriter(f, fieldnames=seadmed[0].keys())
        kirjutaja.writeheader()
        kirjutaja.writerows(tulemus)

    print(f"\nTulemus salvestatud faili: {args.väljund}")