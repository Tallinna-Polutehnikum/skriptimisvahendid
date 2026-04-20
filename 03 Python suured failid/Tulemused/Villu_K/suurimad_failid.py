import os
import csv
from pathlib import Path
from datetime import datetime

def get_file_info(file_path):
    try:
        stats = file_path.stat()
        return {
            "path": str(file_path),
            "size_bytes": stats.st_size,
            "size_mb": round(stats.st_size / (1024 * 1024), 2),
            "size_gb": round(stats.st_size / (1024 * 1024 * 1024), 4),
            "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stats.st_mtime).isoformat()
        }
    except Exception:
        return None

def find_largest_files(directory, top_n=10):
    files = []

    # Define AppData path (Windows)
    appdata_path = Path.home() / "AppData"

    for root, dirs, filenames in os.walk(directory):
        root_path = Path(root)

        # Skip AppData directory entirely
        if appdata_path in root_path.parents or root_path == appdata_path:
            continue

        for name in filenames:
            file_path = root_path / name
            info = get_file_info(file_path)
            if info:
                files.append(info)

    # Sort by size descending
    files.sort(key=lambda x: x["size_bytes"], reverse=True)

    return files[:top_n]

def write_to_csv(data, output_file="suurimad_failid.csv"):
    if not data:
        return

    keys = data[0].keys()

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    home_dir = Path.home()
    largest_files = find_largest_files(home_dir, top_n=10)

    # Print results
    for file in largest_files:
        print(file)

    # Save to CSV
    write_to_csv(largest_files)

    print("\nResults saved to suurimad_failid.csv")