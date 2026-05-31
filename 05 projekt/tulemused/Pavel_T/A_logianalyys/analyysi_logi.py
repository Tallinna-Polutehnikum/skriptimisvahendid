import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def parse_rida(rida: str) -> dict | None:
    """Parsib ühe logirea sõnastikuks. Vigase rea puhul tagastab None."""
    osad = rida.strip().split("\t")

    if len(osad) < 5:
        return None

    ajatempel, staatus, severity, allikas, sonum, *veateade = osad

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
        "viga": veateade[0] if veateade else None,
    }


def loe_logi(tee: Path) -> list[dict]:
    """Loeb logifaili ja jätab vigased read vahele."""
    if not tee.exists():
        raise FileNotFoundError(f"Logifail puudub: {tee}")

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
        print(f"Hoiatus: {vigased} rida ei suutnud parsida")

    return teated


def analuusi(teated: list[dict]) -> dict:
    """Koostab logiteadete põhjal kokkuvõtte."""
    if not teated:
        return {
            "esimene": None,
            "viimane": None,
            "kokku": 0,
            "paevad": {},
            "allikad": Counter(),
            "severity": Counter(),
            "ebaonnestumisi": 0,
        }

    paevad = defaultdict(lambda: Counter())

    for t in teated:
        paev = t["aeg"].date()
        paevad[paev][t["severity"]] += 1
        paevad[paev]["_kokku"] += 1

        if t["staatus"] == "FAIL":
            paevad[paev]["_fail"] += 1

    return {
        "esimene": min(t["aeg"] for t in teated).date(),
        "viimane": max(t["aeg"] for t in teated).date(),
        "kokku": len(teated),
        "paevad": dict(paevad),
        "allikad": Counter(t["allikas"] for t in teated),
        "severity": Counter(t["severity"] for t in teated),
        "ebaonnestumisi": sum(1 for t in teated if t["staatus"] == "FAIL"),
    }


def prindi_kokkuvote(tulemus: dict) -> None:
    """Prindib analüüsi tulemuse konsooli."""
    if tulemus["kokku"] == 0:
        print("Logifail on tühi või ühtegi korrektset rida ei leitud.")
        return

    esimene = tulemus["esimene"]
    viimane = tulemus["viimane"]
    paevade_arv = (viimane - esimene).days + 1
    ok = tulemus["kokku"] - tulemus["ebaonnestumisi"]

    print(f"Periood:        {esimene} kuni {viimane} ({paevade_arv} päeva)")
    print(f"Teateid kokku:  {tulemus['kokku']}")
    print(f"  ├─ õnnestus:   {ok}")
    print(f"  └─ ebaõnnestus: {tulemus['ebaonnestumisi']}")

    print("\nRaskusaste:")
    for nimi in ["Info", "Warning", "Critical"]:
        print(f"  {nimi:<9} {tulemus['severity'].get(nimi, 0)}")

    print("\nTop allikad:")
    for nr, (allikas, arv) in enumerate(tulemus["allikad"].most_common(3), start=1):
        print(f"  {nr}. {allikas:<12} — {arv} teadet")

    print("\nCritical teated päeva lõikes:")
    for paev in sorted(tulemus["paevad"]):
        arv = tulemus["paevad"][paev].get("Critical", 0)
        riba = "██" * arv if arv else "-"
        print(f"  {paev}: {riba} ({arv})")


def salvesta_csv(tulemus: dict, tee: Path) -> None:
    """Salvestab päevade kaupa kokkuvõtte CSV-faili."""
    with open(tee, "w", newline="", encoding="utf-8") as f:
        kirjutaja = csv.writer(f)
        kirjutaja.writerow([
            "Päev",
            "Teateid kokku",
            "Info",
            "Warning",
            "Critical",
            "Ebaõnnestunud",
        ])

        for paev in sorted(tulemus["paevad"]):
            p = tulemus["paevad"][paev]
            kirjutaja.writerow([
                paev,
                p.get("_kokku", 0),
                p.get("Info", 0),
                p.get("Warning", 0),
                p.get("Critical", 0),
                p.get("_fail", 0),
            ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Analüüsi teavituste logifaili")
    parser.add_argument(
        "logi",
        nargs="?",
        default="naidis_ps-alerts.log",
        help="Logifail, vaikimisi naidis_ps-alerts.log",
    )
    parser.add_argument(
        "--valjund",
        default="analyys_paevad.csv",
        help="CSV väljundfail",
    )

    args = parser.parse_args()

    teated = loe_logi(Path(args.logi))
    tulemus = analuusi(teated)
    prindi_kokkuvote(tulemus)
    salvesta_csv(tulemus, Path(args.valjund))

    print(f"\nCSV salvestatud: {args.valjund}")


if __name__ == "__main__":
    main()