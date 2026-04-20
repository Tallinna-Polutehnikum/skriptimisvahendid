from pathlib import Path
import csv

# --- Samm 1: leia kõik failid kodukaustas ---
kodu = Path.home()

failid = []
for fail in kodu.rglob("*"):
    try:
        if fail.is_file():
            failid.append(fail)
    except (PermissionError, OSError):
        continue

# --- Samm 2: sorteeri suuruse järgi ja võta 10 esimest ---
failid_sorditud = []
for fail in failid:
    try:
        suurus = fail.stat().st_size
        failid_sorditud.append((fail, suurus))
    except (PermissionError, OSError, FileNotFoundError):
        continue  # fail kadus vahepeal — jäta vahele

failid_sorditud = sorted(failid_sorditud, key=lambda x: x[1], reverse=True)[:10]

# --- Samm 3: teisenda baidid loetavasse ühikusse ---
def vorminda_suurus(baidid):
    if baidid >= 1_073_741_824:
        return f"{baidid / 1_073_741_824:.1f} GB"
    elif baidid >= 1_048_576:
        return f"{baidid / 1_048_576:.1f} MB"
    else:
        return f"{baidid / 1024:.1f} KB"

# --- Samm 4: ehita iga faili kohta sõnastik ---
tulemus = []

for fail, suurus in failid_sorditud:
    tulemus.append({
        "Tee":    str(fail),
        "Nimi":   fail.name,
        "Suurus": vorminda_suurus(suurus)
    })

# --- Samm 5: salvesta CSV-faili ---
väljund = Path("tulemused/Jan_V/suurimad_failid.csv")
väljund.parent.mkdir(parents=True, exist_ok=True)

with open(väljund, "w", newline="", encoding="utf-8") as f:
    kirjutaja = csv.DictWriter(f, fieldnames=["Tee", "Nimi", "Suurus"])
    kirjutaja.writeheader()
    kirjutaja.writerows(tulemus)

print(f"Salvestatud: {väljund}")
print(f"\n10 suurimat faili:\n")
for rida in tulemus:
    print(f"  {rida['Suurus']:<10} {rida['Nimi']}")