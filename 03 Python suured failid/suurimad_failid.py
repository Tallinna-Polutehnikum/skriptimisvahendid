from pathlib import Path
import csv


def vorminda_suurus(baidid: int) -> str:
    #Teisendab baitide arvu loetavasse ühikusse
    if baidid >= 1_073_741_824:  # 1 GB = 1024^3
        return f"{baidid / 1_073_741_824:.1f} GB"
    elif baidid >= 1_048_576:    # 1 MB = 1024^2
        return f"{baidid / 1_048_576:.1f} MB"
    else:                        # KB
        return f"{baidid / 1024:.1f} KB"


def leia_suurimad_failid(kaust: Path, n: int = 10):
   # käib kausta läbi, kogub failid koos suurusegajätab ligipääsmatud vahele ja tagastab n suurimat
    kandidaadid = []

    for p in kaust.rglob("*"):
        try:
            if p.is_file():
                suurus = p.stat().st_size
                kandidaadid.append((suurus, p))
        except PermissionError:

            continue

    kandidaadid.sort(key=lambda x: x[0], reverse=True)
    return kandidaadid[:n]


def main():
    # kasutaja kodukaust
    kodu = Path.home()

    # leia, sorteeri, võta 10 suurimat
    top10 = leia_suurimad_failid(kodu, n=10)

    #  CSV read
    tulemus = []
    for suurus, fail in top10:
        tulemus.append({
            "Tee": str(fail),
            "Nimi": fail.name,
            "Suurus": vorminda_suurus(suurus)
        })

    # CSV: tulemused\Kaspar_L\

    valjund = Path(__file__).resolve().parent / "Tulemused" / "Kaspar_L" / "suurimad_failid.csv"
    valjund.parent.mkdir(parents=True, exist_ok=True)

    with valjund.open("w", newline="", encoding="utf-8") as f:
        kirjutaja = csv.DictWriter(f, fieldnames=["Tee", "Nimi", "Suurus"])
        kirjutaja.writeheader()
        kirjutaja.writerows(tulemus)

    print(f"Salvestatud: {valjund}")


if __name__ == "__main__":
    main()
