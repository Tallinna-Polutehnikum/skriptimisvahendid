import platform
import socket
import getpass
import psutil
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path


# OS ja host
def kogu_os() -> dict:
    return {
        "süsteem": platform.system(),
        "versioon": platform.version(),
        "release": platform.release(),
        "arhitektuur": platform.architecture()[0],
    }


def kogu_host() -> dict:
    return {
        "host": socket.gethostname(),
        "kasutaja": getpass.getuser(),
        "python": platform.python_version(),
    }


#  CPU 
def kogu_cpu() -> dict:
    mudel = platform.processor()

    # lihtne fallback linuxis
    if not mudel and platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo") as f:
                for rida in f:
                    if "model name" in rida:
                        mudel = rida.split(":")[1].strip()
                        break
        except:
            mudel = "Teadmata"

    return {
        "mudel": mudel or "Teadmata",
        "südamikud_füüsilised": psutil.cpu_count(logical=False),
        "südamikud_loogilised": psutil.cpu_count(logical=True),
        "kasutus_protsent": psutil.cpu_percent(1),
    }


# RAM
def kogu_mälu() -> dict:
    m = psutil.virtual_memory()

    return {
        "kokku_gb": round(m.total / (1024**3), 2),
        "kasutuses_gb": round(m.used / (1024**3), 2),
        "vaba_gb": round(m.available / (1024**3), 2),
        "kasutus_protsent": m.percent,
    }


# kettad
def kogu_kettad() -> list:
    kettad = []

    for osa in psutil.disk_partitions():
        try:
            k = psutil.disk_usage(osa.mountpoint)
        except:
            continue

        kettad.append({
            "haakepunkt": osa.mountpoint,
            "kokku_gb": round(k.total / (1024**3), 2),
            "vaba_gb": round(k.free / (1024**3), 2),
            "kasutus_protsent": k.percent,
        })

    return kettad


# võrk
def kogu_võrk() -> list:
    tulem = []
    aadressid = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for nimi, adrlist in aadressid.items():
        ipv4 = None

        # parsing ipv4
        for a in adrlist:
            if a.family == socket.AF_INET and not a.address.startswith("127."):
                ipv4 = a.address

        on = stats[nimi].isup if nimi in stats else False

        tulem.append({
            "nimi": nimi,
            "ipv4": ipv4,
            "ühendatud": on
        })

    return tulem


# print
def prindi(inv: dict):
    print("=== Süsteemi inventuur ===")
    print(f"Host:        {inv['host']}")
    print(f"Kasutaja:    {inv['kasutaja']}")
    print(f"OS:          {inv['os']['süsteem']} {inv['os']['release']} ({inv['os']['versioon']})")
    print(f"Python:      {inv['python']}\n")

    print(f"CPU:         {inv['cpu']['mudel']}")
    print(f"Südamikke:   {inv['cpu']['südamikud_füüsilised']} ({inv['cpu']['südamikud_loogilised']} loogilist)")
    print(f"RAM:         {inv['mälu']['kokku_gb']} GB (kasutuses {inv['mälu']['kasutus_protsent']}%)\n")

    print("Kettad:")
    for k in inv["kettad"]:
        vaba = 100 - k["kasutus_protsent"]
        print(f"  {k['haakepunkt']:<6} Free: {k['vaba_gb']} GB ({round(vaba)}%)")

    print("\nVõrgukaardid:")
    for v in inv["võrk"]:
        ip = v["ipv4"] if v["ipv4"] else "(ühendamata)"
        print(f"  {v['nimi']:<20} {ip}")


# main
def main():
    parser = argparse.ArgumentParser(description="Süsteemi inventuur")
    parser.add_argument("--väljund", help="JSON-fail (vaikimisi automaatselt)")
    parser.add_argument("--stdout", action="store_true",
                        help="Prindi JSON konsooli, ära salvesta faili")
    args = parser.parse_args()

    inv = {
        "ajamäär": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        **kogu_host(),
        "os": kogu_os(),
        "cpu": kogu_cpu(),
        "mälu": kogu_mälu(),
        "kettad": kogu_kettad(),
        "võrk": kogu_võrk(),
    }

    if args.stdout:
        print(json.dumps(inv, indent=2, ensure_ascii=False))
        return

    prindi(inv)

    # fail
    if args.väljund:
        path = Path(args.väljund)
    else:
        kp = datetime.now().strftime("%Y-%m-%d")
        path = Path(f"inventuur_{inv['host']}_{kp}.json")

    path.write_text(json.dumps(inv, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSalvestatud: {path}")


if __name__ == "__main__":
    main()