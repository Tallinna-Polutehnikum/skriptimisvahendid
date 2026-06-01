import argparse
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
import csv


def parse_rida(rida: str) -> dict | None:
    osad = rida.strip().split("\t")

    if len(osad) < 5:
        return None

    ajatempel, staatus, severity, allikas, sonum, *viga = osad

    try:
        aeg = datetime.strptime(ajatempel, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

    return {
        "aeg": aeg,
        "staatus": staatus.strip("[]"),
        "severity": severity,
        "allikas": allikas,
        "sonum": sonum,
        "viga": viga[0] if viga else None
    }


def loe_logi(tee: Path) -> list[dict]:
    if not tee.exists():
        print(f"Logifail puudub: {tee}")
        return []

    teated = []
    vigased = 0

    for rida in tee.read_text(encoding="utf-8").splitlines():
        if not rida.strip():
            continue

        parsed = parse_rida(rida)
        if parsed:
            teated.append(parsed)
        else:
            vigased += 1

    if vigased:
        print(f"Hoiatus: {vigased} vigast rida")

    return teated


def analuusi(teated: list[dict]) -> dict:
    if not teated:
        return {
            "kokku": 0,
            "paevad": {},
            "allikad": Counter(),
            "severity": Counter(),
            "ebaonnestumisi": 0
        }

    paevad = defaultdict(lambda: Counter())

    for t in teated:
        paev = t["aeg"].date()

        paevad[paev]["_kokku"] += 1
        paevad[paev][t["severity"]] += 1

        if t["staatus"] == "FAIL":
            paevad[paev]["_fail"] += 1

    return {
        "esimene": min(t["aeg"] for t in teated).date(),
        "viimane": max(t["aeg"] for t in teated).date(),
        "kokku": len(teated),
        "paevad": dict(paevad),
        "allikad": Counter(t["allikas"] for t in teated),
        "severity": Counter(t["severity"] for t in teated),
        "ebaonnestumisi": sum(1 for t in teated if t["staatus"] == "FAIL")
    }


def prindi_kokkuvote(tulemus: dict):
    if tulemus["kokku"] == 0:
        print("Logi on tühi.")
        return

    print(f"Periood: {tulemus['esimene']} kuni {tulemus['viimane']}")
    print(f"Teateid kokku: {tulemus['kokku']}")
    print(f"Õnnestus: {tulemus['kokku'] - tulemus['ebaonnestumisi']}")
    print(f"Ebaõnnestus: {tulemus['ebaonnestumisi']}")

    print("\nRaskusaste:")
    for k, v in tulemus["severity"].items():
        print(f"  {k}: {v}")

    print("\nTop allikad:")
    for nimi, arv in tulemus["allikad"].most_common(3):
        print(f"  {nimi} — {arv}")

    print("\nCritical teated päeva lõikes:")
    for paev in sorted(tulemus["paevad"]):
        arv = tulemus["paevad"][paev].get("Critical", 0)
        riba = "██" * arv if arv else "-"
        print(f"  {paev}: {riba}")


def salvesta_csv(tulemus: dict, tee: Path):
    with open(tee, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Paev", "Kokku", "Info", "Warning", "Critical", "Fail"])

        for paev in sorted(tulemus["paevad"]):
            p = tulemus["paevad"][paev]

            w.writerow([
                paev,
                p.get("_kokku", 0),
                p.get("Info", 0),
                p.get("Warning", 0),
                p.get("Critical", 0),
                p.get("_fail", 0)
            ])


def main():
    parser = argparse.ArgumentParser(description="Logianaluus")
    parser.add_argument("logi", nargs="?", default="ps-alerts.log")
    parser.add_argument("--valjund", default="analyys_paevad.csv")

    args = parser.parse_args()

    teated = loe_logi(Path(args.logi))
    tulemus = analuusi(teated)

    prindi_kokkuvote(tulemus)
    salvesta_csv(tulemus, Path(args.valjund))

    print(f"\nCSV salvestatud: {args.valjund}")


if __name__ == "__main__":
    main()