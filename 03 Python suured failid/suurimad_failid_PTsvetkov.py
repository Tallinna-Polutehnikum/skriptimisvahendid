from pathlib import Path
import csv


def vorminda_suurus(baidid):
    if baidid >= 1_073_741_824:
        return f"{baidid / 1_073_741_824:.1f} GB"
    elif baidid >= 1_048_576:
        return f"{baidid / 1_048_576:.1f} MB"
    else:
        return f"{baidid / 1024:.1f} KB"


kodu = Path.home()
failid = []

for fail in kodu.rglob("*"):
    try:
        if fail.is_file():
            suurus = fail.stat().st_size
            failid.append((fail, suurus))
    except (PermissionError, FileNotFoundError):
        continue

failid_sorditud = sorted(
    failid,
    key=lambda x: x[1],
    reverse=True
)[:10]

tulemus = []

for fail, suurus in failid_sorditud:
    tulemus.append({
        "Tee": str(fail),
        "Nimi": fail.name,
        "Suurus": vorminda_suurus(suurus)
    })

print("\n10 kõige suuremat faili:")
for rida in tulemus:
    print(f"{rida['Nimi']} -> {rida['Suurus']}")
    
valjund = Path("tulemused/Pavel_T/suurimad_failid.csv")
valjund.parent.mkdir(parents=True, exist_ok=True)

with open(valjund, "w", newline="", encoding="utf-8") as f:
    kirjutaja = csv.DictWriter(f, fieldnames=["Tee", "Nimi", "Suurus"])
    kirjutaja.writeheader()
    kirjutaja.writerows(tulemus)

print(f"Salvestatud: {valjund}")