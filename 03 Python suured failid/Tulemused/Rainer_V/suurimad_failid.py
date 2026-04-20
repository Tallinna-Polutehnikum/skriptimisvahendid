import argparse
import csv
from datetime import datetime
from pathlib import Path


def parsi_argumendid():
    parser = argparse.ArgumentParser(
        description="Leia 10 suurimat faili ja salvesta tulemused CSV-faili."
    )
    parser.add_argument(
        "otsingukoht",
        nargs="?",
        default=str(Path.home()),
        help="Kaust, kust rekursiivselt faile otsida (vaikimisi kasutaja kodukaust).",
    )
    return parser.parse_args()


def loetav_suurus(suurus_b):
    if suurus_b >= 1024 ** 3:
        return f"{suurus_b / (1024 ** 3):.1f} GB"
    if suurus_b >= 1024 ** 2:
        return f"{suurus_b / (1024 ** 2):.1f} MB"
    if suurus_b >= 1024:
        return f"{suurus_b / 1024:.1f} KB"
    return f"{suurus_b} B"


args = parsi_argumendid()
root = Path(args.otsingukoht).expanduser()

if not root.exists() or not root.is_dir():
    raise SystemExit(f"Otsingukoht ei ole olemas või ei ole kaust: {root}")

failid = []

for fail in root.rglob("*"):
    try:
        # Välista AppData
        if "AppData" in fail.parts:
            continue

        # Võta ainult failid
        if not fail.is_file():
            continue

        stat = fail.stat()
    except (PermissionError, OSError):
        continue

    failid.append(
        {
            "tee": fail,
            "suurus_baitides": stat.st_size,
            "muudetud_aeg": stat.st_mtime,
        }
    )

# Sorteeri failid suuruse järgi (suurim -> väikseim) ja võta 10 esimest
top_10 = sorted(failid, key=lambda f: f["suurus_baitides"], reverse=True)[:10]

failide_andmed = []

for faili_info in top_10:
    fail = faili_info["tee"]
    suurus_b = faili_info["suurus_baitides"]
    muudetud = datetime.fromtimestamp(faili_info["muudetud_aeg"]).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    faili_dict = {
        "Tee": str(fail),
        "Nimi": fail.name,
        "Suurus": loetav_suurus(suurus_b),
        "Muudetud": muudetud,
    }
    failide_andmed.append(faili_dict)

skripti_kaust = Path(__file__).resolve().parent
csv_fail = skripti_kaust / "suurimad_failid.csv"

with csv_fail.open("w", newline="", encoding="utf-8") as f:
    kirjutaja = csv.DictWriter(f, fieldnames=["Tee", "Nimi", "Suurus", "Muudetud"])
    kirjutaja.writeheader()
    kirjutaja.writerows(failide_andmed)

print(f"Tulemus salvestatud: {csv_fail.resolve()}")