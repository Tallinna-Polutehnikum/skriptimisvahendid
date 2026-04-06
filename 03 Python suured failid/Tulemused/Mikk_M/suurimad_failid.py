import csv
from pathlib import Path
from datetime import datetime

# Samm 1 — leia kõik failid kodukaustas

kodukaust = Path.home()
failid = []
for fail in kodukaust.rglob("*"):
    try:
        if fail.is_file():
            if "AppData" in fail.parts:
                continue
            failid.append(fail)
    except PermissionError:
        continue


# Samm 2 — sorteeri suuruse järgi ja võta 10 esimest

failid = sorted(failid, key=lambda f: f.stat().st_size, reverse=True)[:10]

# Samm 3 — teisenda baidid loetavasse ühikusse

def suurus_loetav(suurus_baitides):
    if suurus_baitides >= 1_073_741_824:
        return f"{suurus_baitides/1_073_741_824:.1f} GB"
    elif suurus_baitides >= 1_048_576:
        return f"{suurus_baitides/1_048_576:.1f} MB"
    elif suurus_baitides >= 1024:
        return f"{suurus_baitides/1024:.1f} KB"
    else:
        return f"{suurus_baitides} B"


# Samm 4 — ehita iga faili kohta sõnastik

andmed = []
for f in failid:
    stat = f.stat()
    andmed.append({
        "Tee": str(f.resolve()),
        "Nimi": f.name,
        "Suurus": suurus_loetav(stat.st_size),
        "Muudetud": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    })


# Samm 5 — salvesta CSV-faili

väljundkaust = Path("Tulemused/Mikk_M")
väljundkaust.mkdir(parents=True, exist_ok=True)

väljundfail = väljundkaust / "suurimad_failid.csv"

with open(väljundfail, "w", newline="", encoding="utf-8") as f:
    väljad = ["Tee", "Nimi", "Suurus", "Muudetud"]
    kirjutaja = csv.DictWriter(f, fieldnames=väljad)
    kirjutaja.writeheader()
    kirjutaja.writerows(andmed)

print(f"Tulemus salvestatud: {väljundfail}")