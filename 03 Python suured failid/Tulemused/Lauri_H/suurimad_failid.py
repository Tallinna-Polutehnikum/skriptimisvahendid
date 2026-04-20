from pathlib import Path
import csv
from datetime import datetime
import argparse

# ----------------------------
# Argumendid (käsurealt kaust)
# ----------------------------
parser = argparse.ArgumentParser(description="Leia 10 suurimat faili")
parser.add_argument(
    "path",
    nargs="?",
    default=Path.home(),
    help="Kaust, kust otsida (vaikimisi kodukaust)"
)

args = parser.parse_args()
search_path = Path(args.path)

# ----------------------------
# Funktsioon: loetav suurus
# ----------------------------
def human_readable(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

# ----------------------------
# Failide kogumine
# ----------------------------
files_with_size = []

for f in search_path.rglob("*"):
    if not f.is_file():
        continue

    # Välista AppData
    if "AppData" in f.parts:
        continue

    try:
        stat = f.stat()
        size = stat.st_size
        modified_time = datetime.fromtimestamp(stat.st_mtime)

        files_with_size.append((f, size, modified_time))

    except (FileNotFoundError, PermissionError):
        continue

# ----------------------------
# Sorteerimine ja TOP 10
# ----------------------------
files_sorted = sorted(files_with_size, key=lambda x: x[1], reverse=True)
top10 = files_sorted[:10]

# ----------------------------
# Väljundkaust
# ----------------------------
output_dir = Path("tulemused/Lauri_H")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "suurimad_failid.csv"

# ----------------------------
# CSV kirjutamine
# ----------------------------
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["Tee", "Failinimi", "Suurus", "Muudetud"])

    for file, size, modified_time in top10:
        writer.writerow([
            file,
            file.name,
            human_readable(size),
            modified_time.strftime("%Y-%m-%d %H:%M:%S")
        ])

# ----------------------------
# Lõpp
# ----------------------------
print("Valmis! Tulemused salvestatud:", output_file)