import os
from datetime import datetime

kaust = "failide-harjutus"

print("Failid enne ümbernimetamist:")
print("-" * 35)

for failinimi in sorted(os.listdir(kaust)):
    print(failinimi)

print()
print("Nimetan failid ümber...")
print("-" * 35)

kuupaev = datetime.now().strftime("%Y-%m-%d")

for failinimi in os.listdir(kaust):
    vana_tee = os.path.join(kaust, failinimi)

    nimi = failinimi.lower()
    nimi = nimi.replace(" ", "_")

    # Kui kuupäev on juba failinime alguses, eemaldame selle enne uue nime koostamist.
    if nimi.startswith(kuupaev + "_"):
        nimi = nimi[len(kuupaev) + 1:]

    # Kui eesliide on juba olemas, eemaldame selle enne uue nime koostamist.
    if nimi.startswith("pilt_"):
        nimi = nimi[len("pilt_"):]
    elif nimi.startswith("tekst_"):
        nimi = nimi[len("tekst_"):]

    if nimi.endswith(".jpg"):
        nimi = "pilt_" + nimi
    elif nimi.endswith(".txt"):
        nimi = "tekst_" + nimi
    else:
        continue

    uus_nimi = f"{kuupaev}_{nimi}"
    uus_tee = os.path.join(kaust, uus_nimi)

    if failinimi != uus_nimi:
        os.rename(vana_tee, uus_tee)
        print(f"  {failinimi}  →  {uus_nimi}")

print()
print("Failid pärast ümbernimetamist:")
print("-" * 35)

for failinimi in sorted(os.listdir(kaust)):
    print(failinimi)

# Kui skripti käivitada mitu korda, siis ilma kontrollita lisataks
# kuupäev ja eesliited failinimele iga kord uuesti.
# Selle vältimiseks kontrollime kõigepealt, kas kuupäev või eesliide
# on juba olemas, eemaldame need vajadusel, ja ehitame failinime
# seejärel uuesti korrektselt kokku.