import os
import csv

home_dir = os.path.expanduser("~") # root directory of current user

files = []

for root, dirs, filenames in os.walk(home_dir):
    for file in filenames:
        try:
            full_path = os.path.join(root, file)
            size = os.path.getsize(full_path)
            files.append((full_path, file, size))

        except (PermissionError, FileNotFoundError):
            continue
files.sort(key=lambda x: x[2], reverse=True) # Sort

top_15 = files[:15]

# Convert bytes to human format
def format_size(size):
    if size >= 1024**3:
        return f"{size / (1024**3):.1f} GB"
    elif size >= 1024**2:
        return f"{size / (1024**2):.1f} MB"
    else:
        return f"{size / 1024:.1f} KB"

# Kuidas täpsemalt ma võin teha faili directory loomist, ei tea. Tegin nii pidi.
output_dir = os.path.join("tulemused", "Juri_P")  
os.makedirs(output_dir, exist_ok=True)

csv_file = os.path.join(output_dir, "suurimad_failid.csv") # csv faili loomine

# Row converter
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["Tee", "Nimi", "Suurus"])

    for path, name, size in top_15:
        writer.writerow([path, name, format_size(size)])

print(f"Tulemus salvestatud: {csv_file}") # Tulemus koos faili nimetusega