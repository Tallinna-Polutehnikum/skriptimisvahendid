from pathlib import Path
import csv

def loetav_suurus(baitides):
    if baitides >= 1024**3:
        return f"{baitides / (1024**3):.1f} GB"
    elif baitides >= 1024**2:
        return f"{baitides / (1024**2):.1f} MB"
    elif baitides >= 1024:
        return f"{baitides / 1024:.1f} KB"
    else:
        return f"{baitides} B"

# 1) Otsing kodukaustas
kodu = Path.home()
failid = []

for fail in kodu.rglob("*"):
    try:
        if fail.is_file():
            failid.append(fail)
    except PermissionError:
        continue

# 2) Sorteeri ja võta 10 suurimat
suurimad = sorted(failid, key=lambda f: f.stat().st_size, reverse=True)[:10]

# 3) Ehita andmed CSV jaoks
andmed = []
for f in suurimad:
    suurus = loetav_suurus(f.stat().st_size)
    andmed.append({
        "Tee": str(f),
        "Nimi": f.name,
        "Suurus": suurus
    })

# 4) Loo väljundkaust
valjund_kaust = Path("03 Python suured failid") / "tulemused" / "Martin_E"
valjund_kaust.mkdir(parents=True, exist_ok=True)

# 5) Salvesta CSV
csv_fail = valjund_kaust / "suurimad_failid.csv"

with open(csv_fail, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Tee", "Nimi", "Suurus"])
    writer.writeheader()
    writer.writerows(andmed)

print("Valmis! Fail salvestatud:", csv_fail)