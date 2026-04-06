import os
import csv

home_dir = os.path.expanduser("~")
files_with_size = []

for root, dirs, files in os.walk(home_dir):
    for name in files:
        try:
            full_path = os.path.join(root, name)
            size = os.path.getsize(full_path)
            # Salvestame listi kolm asja: suurus, tee ja failinimi
            files_with_size.append((size, root, name))
        except (PermissionError, FileNotFoundError):
            continue

# Sorteerime suuruse järgi
files_with_size.sort(reverse=True, key=lambda x: x[0])

top_10 = files_with_size[:10]

def format_size(size_bytes):
    if size_bytes >= 1024**3:
        return f"{size_bytes / (1024**3):.2f} GB"
    elif size_bytes >= 1024**2:
        return f"{size_bytes / (1024**2):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} B"

# Tulemuste printimine ekraanile
print("Top 10 suurimat faili:\n")
for size, path, name in top_10:
    full_path = os.path.join(path, name)
    print(f"{format_size(size)} - {full_path}")

# CSV-sse eksportimine
# Märkus: __file__ töötab ainult skriptina käivitades, mitte interaktiivses konsoolis
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = os.getcwd()

csv_file = os.path.join(base_dir, "suurimad_failid.csv")

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # Päis - lisatud faili nimi ja tee eraldi
    writer.writerow(["Faili nimi", "Täis tee", "Suurus baitides", "Loetav suurus"])
    
    # Andmed
    for size, path, name in top_10:
        full_path = os.path.join(path, name)
        writer.writerow([name, full_path, size, format_size(size)])

print(f"\nAndmed eksporditud faili: {csv_file}")