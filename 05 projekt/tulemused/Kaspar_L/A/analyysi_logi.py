import argparse
from pathlib import Path
from datetime import datetime
import csv


# parsib ühe rea
def parse_rida(rida):
    osad = rida.strip().split("\t")

    if len(osad) < 5:
        return None

    ajatempel = osad[0]
    staatus = osad[1]
    severity = osad[2]
    allikas = osad[3]
    sonum = osad[4]

    veateade = None
    if len(osad) > 5:
        veateade = osad[5]

    try:
        aeg = datetime.strptime(ajatempel, "%Y-%m-%d %H:%M:%S")
    except:
        return None

    return {
        "aeg": aeg,
        "staatus": staatus.strip("[]"),
        "severity": severity,
        "allikas": allikas,
        "sonum": sonum,
        "viga": veateade
    }


# loeb faili
def loe_logi(tee):
    if not tee.exists():
        print("faili pole")
        return []

    teated = []
    vigased = 0

    for rida in tee.read_text(encoding="utf-8").splitlines():
        if rida.strip() == "":
            continue

        parsed = parse_rida(rida)

        if parsed != None:
            teated.append(parsed)
        else:
            vigased += 1

    if vigased > 0:
        print("hoiatus, vigaseid ridu:", vigased)

    return teated


# analüüs
def analyysi(teated):
    if len(teated) == 0:
        return {"kokku": 0, "paevad": {}}

    paevad = {}
    severity = {}
    allikad = {}

    esimene = None
    viimane = None

    failid = 0

    for t in teated:
        paev = t["aeg"].date()

        if paev not in paevad:
            paevad[paev] = {"_kokku": 0, "_fail": 0}

        paevad[paev]["_kokku"] += 1

        # severity per päev
        s = t["severity"]
        if s not in paevad[paev]:
            paevad[paev][s] = 0
        paevad[paev][s] += 1

        # üldine severity
        if s not in severity:
            severity[s] = 0
        severity[s] += 1

        # allikad
        a = t["allikas"]
        if a not in allikad:
            allikad[a] = 0
        allikad[a] += 1

        # fail
        if t["staatus"] == "FAIL":
            paevad[paev]["_fail"] += 1
            failid += 1

        # periood
        if esimene == None or paev < esimene:
            esimene = paev
        if viimane == None or paev > viimane:
            viimane = paev

    return {
        "kokku": len(teated),
        "paevad": paevad,
        "severity": severity,
        "allikad": allikad,
        "fail": failid,
        "esimene": esimene,
        "viimane": viimane
    }


# ascii riba
def riba(n):
    if n == 0:
        return "-"
    return "██" * n


# print
def prindi(t):
    if t["kokku"] == 0:
        print("tühi logi")
        return

    print("Periood:", t["esimene"], "kuni", t["viimane"])
    print("Teateid kokku:", t["kokku"])
    print("õnnestus:", t["kokku"] - t["fail"])
    print("ebaõnnestus:", t["fail"])

    print("\nRaskusaste:")
    for x in ["Info", "Warning", "Critical"]:
        print(x, ":", t["severity"].get(x, 0))

    print("\nTop allikad:")
    sorted_allikad = sorted(t["allikad"].items(), key=lambda x: x[1], reverse=True)
    nr = 1
    for a, c in sorted_allikad[:3]:
        print(nr, a, "-", c)
        nr += 1

    print("\nCritical teated päeva lõikes:")
    for p in sorted(t["paevad"].keys()):
        c = t["paevad"][p].get("Critical", 0)
        print(p, ":", riba(c), f"({c})")


# csv 
def salvesta_csv(t, tee):
    with open(tee, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        w.writerow(["Päev", "Teateid kokku", "Info", "Warning", "Critical", "Ebaõnnestunud"])

        for paev in sorted(t["paevad"].keys()):
            p = t["paevad"][paev]

            w.writerow([
                paev,
                p.get("_kokku", 0),
                p.get("Info", 0),
                p.get("Warning", 0),
                p.get("Critical", 0),
                p.get("_fail", 0)
            ])


# main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logi", nargs="?", default="ps-alerts.log")
    parser.add_argument("--valjund", default="analyys_paevad.csv")
    args = parser.parse_args()

    teated = loe_logi(Path(args.logi))
    tulemus = analyysi(teated)

    prindi(tulemus)
    salvesta_csv(tulemus, Path(args.valjund))

    print("\nCSV salvestatud:", args.valjund)


if __name__ == "__main__":
    main()