import json
import platform
import socket
import psutil

info = {
    "os": platform.system(),
    "os_version": platform.version(),
    "processor": platform.processor(),
    "hostname": socket.gethostname(),
    "python_version": platform.python_version(),
    "cpu_cores": psutil.cpu_count(),
    "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    "disk_total_gb": round(psutil.disk_usage("/").total / (1024**3), 2),
    "disk_free_gb": round(psutil.disk_usage("/").free / (1024**3), 2),
    "network_interfaces": list(psutil.net_if_addrs().keys())
}

with open("inventuur.json", "w", encoding="utf-8") as f:
    json.dump(info, f, indent=4)

print("Inventuur salvestatud: inventuur.json")