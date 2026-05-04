from pathlib import Path
import csv

# 1. Määra kodukaust
kodu = Path.home()

failid = []

# 2. Leia kõik failid rekursiivselt
for fail in kodu.rglob("*"):
    try:
        # Välista kaustad ja probleemsed kohad (nt AppData)
        if fail.is_file() and "AppData" not in fail.parts:
            failid.append(fail)
    except PermissionError:
        continue  # kui ligipääsu pole, liigu edasi

# 3. Sorteeri suuruse järgi (suurim ees) ja võta top 10
failid_sorditud = sorted(
    failid,
    key=lambda f: f.stat().st_size,
    reverse=True
)[:10]

# 4. Funktsioon suuruse vormindamiseks
def vorminda_suurus(baidid):
    if baidid >= 1_073_741_824:
        return f"{baidid / 1_073_741_824:.1f} GB"
    elif baidid >= 1_048_576:
        return f"{baidid / 1_048_576:.1f} MB"
    else:
        return f"{baidid / 1024:.1f} KB"

# 5. Koosta tulemused
tulemus = []

for fail in failid_sorditud:
    try:
        suurus = fail.stat().st_size
        tulemus.append({
            "Tee": str(fail),
            "Nimi": fail.name,
            "Suurus": vorminda_suurus(suurus)
        })
    except PermissionError:
        continue

# 6. Salvesta CSV faili
valjund = Path("tulemused/Tarmo_M/suurimad_failid.csv")
valjund.parent.mkdir(parents=True, exist_ok=True)

with open(valjund, "w", newline="", encoding="utf-8") as f:
    kirjutaja = csv.DictWriter(f, fieldnames=["Tee", "Nimi", "Suurus"])
    kirjutaja.writeheader()
    kirjutaja.writerows(tulemus)

# 7. Väljasta tulemus
print("Top 10 suurimat faili:")
for rida in tulemus:
    print(f"{rida['Nimi']} — {rida['Suurus']}")

print(f"\nSalvestatud: {valjund}")