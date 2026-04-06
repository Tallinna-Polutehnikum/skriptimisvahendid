from datetime import datetime
import os

kaust = "failide-harjutus"
tana = datetime.now().strftime("%Y-%m-%d")

for failinimi in os.listdir(kaust):
    uus_nimi = failinimi

    # 1. väiketähed
    uus_nimi = uus_nimi.lower()

    # 2. tühikud
    uus_nimi = uus_nimi.replace(" ", "_")

    # 3. prefiks
    if uus_nimi.endswith(".jpg") and not uus_nimi.startswith("pilt_"):
        uus_nimi = "pilt_" + uus_nimi
    elif uus_nimi.endswith(".txt") and not uus_nimi.startswith("tekst_"):
        uus_nimi = "tekst_" + uus_nimi

    # 4. kuupäev
    if not uus_nimi.startswith(tana):
        uus_nimi = f"{tana}_{uus_nimi}"

    # ümbernimetamine ainult siis kui vaja
    if uus_nimi != failinimi:
        vana_tee = os.path.join(kaust, failinimi)
        uus_tee  = os.path.join(kaust, uus_nimi)
        os.rename(vana_tee, uus_tee)
        print(f"{failinimi} → {uus_nimi}")