import platform
import socket
import getpass
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

import psutil


def kogu_host():
    return {
        "host": socket.gethostname(),
        "kasutaja": getpass.getuser(),
        "python": platform.python_version(),
    }


def kogu_os():
    return {
        "süsteem": platform.system(),
        "versioon": platform.version(),
        "release": platform.release(),
        "arhitektuur": platform.architecture()[0],
    }


def kogu_cpu():
    return {
        "mudel": platform.processor() or "Teadmata",
        "südamikud_füüsilised": psutil.cpu_count(logical=False),
        "südamikud_loogilised": psutil.cpu_count(logical=True),
        "kasutus_protsent": psutil.cpu_percent(interval=1),
    }


def kogu_mälu():
    m = psutil.virtual_memory()
    return {
        "kokku_gb": round(m.total / (1024**3), 2),
        "kasutuses_gb": round(m.used / (1024**3), 2),
        "vaba_gb": round(m.available / (1024**3), 2),
        "kasutus_protsent": m.percent,
    }


def kogu_kettad():
    kettad = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except Exception:
            continue

        kettad.append({
            "haakepunkt": part.mountpoint,
            "seade": part.device,
            "failisüsteem": part.fstype,
            "kokku_gb": round(usage.total / (1024**3), 2),
            "vaba_gb": round(usage.free / (1024**3), 2),
            "kasutus_protsent": usage.percent,
        })
    return kettad


def kogu_võrk():
    kaardid = []
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for name, addr_list in addrs.items():
        ipv4 = None

        for a in addr_list:
            if a.family == socket.AF_INET and not a.address.startswith("127."):
                ipv4 = a.address

        is_up = stats[name].isup if name in stats else False

        kaardid.append({
            "nimi": name,
            "ipv4": ipv4,
            "ühendatud": is_up,
        })

    return kaardid


def prindi_kokkuvote(data):
    print("=== Süsteemi inventuur ===")
    print(f"Host:        {data['host']}")
    print(f"Kasutaja:    {data['kasutaja']}")
    print(f"OS:          {data['os']['süsteem']} ({data['os']['release']})")
    print(f"Python:      {data['python']}")
    print()

    print(f"CPU:         {data['cpu']['mudel']}")
    print(f"Südamikke:   {data['cpu']['südamikud_füüsilised']} ({data['cpu']['südamikud_loogilised']} loogilist)")
    print(f"RAM:         {data['mälu']['kokku_gb']} GB ({data['mälu']['kasutus_protsent']}%)")
    print()

    print("Kettad:")
    for d in data["kettad"]:
        print(f"  {d['haakepunkt']}  Total: {d['kokku_gb']} GB  Free: {d['vaba_gb']} GB ({100 - d['kasutus_protsent']}% vaba)")

    print()
    print("Võrgukaardid:")
    for v in data["võrk"]:
        ip = v["ipv4"] if v["ipv4"] else "(ühendamata)"
        print(f"  {v['nimi']:15} {ip}")


def main():
    parser = argparse.ArgumentParser(description="Süsteemi inventuur")
    parser.add_argument("--väljund", help="JSON faili nimi")
    parser.add_argument("--stdout", action="store_true", help="Näita JSON konsoolis")
    args = parser.parse_args()

    data = {
        "ajamäär": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        **kogu_host(),
        "os": kogu_os(),
        "cpu": kogu_cpu(),
        "mälu": kogu_mälu(),
        "kettad": kogu_kettad(),
        "võrk": kogu_võrk(),
    }

    if args.stdout:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    prindi_kokkuvote(data)

    if args.väljund:
        output = Path(args.väljund)
    else:
        name = f"inventuur_{data['host']}_{datetime.now().strftime('%Y-%m-%d')}.json"
        output = Path(name)

    output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nSalvestatud: {output}")


if __name__ == "__main__":
    main()