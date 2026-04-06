import os

kaust = os.path.join(os.path.dirname(__file__), "failide-harjutus")

print("Failid enne ümbernimetamist:")
print("-" * 35)

failid = os.listdir(kaust)
for failinimi in failid:
    print(failinimi)

print()
print("Nimetan tühikud allkriipsudeks...")
print("-" * 35)

for failinimi in os.listdir(kaust):
    if " " in failinimi:
        uus_nimi = failinimi.replace(" ", "_")

        vana_tee = os.path.join(kaust, failinimi)
        uus_tee = os.path.join(kaust, uus_nimi)

        os.rename(vana_tee, uus_tee)
        print(f"  {failinimi}  →  {uus_nimi}")

print()
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
    uus_tee = os.path.join(kaust, uus_nimi)

    os.rename(vana_tee, uus_tee)
    print(f"  {failinimi}  →  {uus_nimi}")

print()
print("Failid pärast ümbernimetamist:")
print("-" * 35)

for failinimi in sorted(os.listdir(kaust)):
    print(failinimi)