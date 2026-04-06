import os
import datetime

kaust = "failide-harjutus"

print("Failid enne ümbernimetamist:")
print("-" * 35)
failid = os.listdir(kaust)
for failinimi in failid:
    print(failinimi)

print("Nimetan tühikud allkriipsudeks...")
print("-" * 35)
for failinimi in os.listdir(kaust):
    if " " in failinimi:
        uus_nimi = failinimi.replace(" ", "_")
        vana_tee = os.path.join(kaust, failinimi)
        uus_tee  = os.path.join(kaust, uus_nimi)
        os.rename(vana_tee, uus_tee)
        print(f"  {failinimi}  →  {uus_nimi}")

print("Muudan failinimed väiketähtedeks...")
print("-" * 35)
for failinimi in os.listdir(kaust):
    uus_nimi = failinimi.lower()
    if uus_nimi != failinimi:
        vana_tee = os.path.join(kaust, failinimi)
        uus_tee  = os.path.join(kaust, uus_nimi)
        os.rename(vana_tee, uus_tee)
        print(f"  {failinimi}  →  {uus_nimi}")

print("Lisan eesliited failitüübi järgi...")
print("-" * 35)
for failinimi in os.listdir(kaust):
    if failinimi.endswith(".jpg") and not failinimi.startswith("pilt_"):
        uus_nimi = "pilt_" + failinimi
    elif failinimi.endswith(".txt") and not failinimi.startswith("tekst_"):
        uus_nimi = "tekst_" + failinimi
    else:
        continue
    vana_tee = os.path.join(kaust, failinimi)
    uus_tee  = os.path.join(kaust, uus_nimi)
    os.rename(vana_tee, uus_tee)
    print(f"  {failinimi}  →  {uus_nimi}")

print("Lisan kuupäeva eesliiteks...")
print("-" * 35)
tanapäev = datetime.date.today().strftime("%Y-%m-%d")
for failinimi in os.listdir(kaust):
    if not failinimi.startswith(tanapäev):  # väldib topelt lisamist!
        uus_nimi = tanapäev + "_" + failinimi
        vana_tee = os.path.join(kaust, failinimi)
        uus_tee  = os.path.join(kaust, uus_nimi)
        os.rename(vana_tee, uus_tee)
        print(f"  {failinimi}  →  {uus_nimi}")

print("Failid pärast ümbernimetamist:")
print("-" * 35)
for failinimi in sorted(os.listdir(kaust)):
    print(failinimi)
