import os  # os-moodul võimaldab failide ja kaustadega töötada
from datetime import date

kaust = "failide-harjutus"  # kaust, milles tegutseme

print("Failid enne ümbernimetamist:")
print("-" * 35)

failid = os.listdir(kaust)   # tagastab nimekirja kaustas olevatest failidest
for failinimi in failid:
    print(failinimi)

# Korduval käivitamisel võib tekkida olukord, kus failinimed on juba ümber nimetatud ja seda tehakse uuesti.
# Vältimiseks peaks lisama eelkontrollid, mis kontrollivad, kas üldse on vaja midagi ümber nimetada.

print("Nimetan tühikud allkriipsudeks...")
print("-" * 35)

for failinimi in os.listdir(kaust):

    if " " in failinimi:  # kontrolli, kas failinimi sisaldab tühikut

        uus_nimi = failinimi.replace(" ", "_")  # asenda kõik tühikud

        vana_tee = os.path.join(kaust, failinimi)  # täielik tee vanale failile
        uus_tee  = os.path.join(kaust, uus_nimi)   # täielik tee uuele failile

        os.rename(vana_tee, uus_tee)  # teeb ümbernimetamise

        print(f"  {failinimi}  →  {uus_nimi}")

print("Lisan eesliited failitüübi järgi...")
print("-" * 35)

for failinimi in os.listdir(kaust):

    if failinimi.endswith(".jpg") and not failinimi.startswith("pilt_"):
        uus_nimi = "pilt_" + failinimi

    elif failinimi.endswith(".txt") and not failinimi.startswith("tekst_"):
        uus_nimi = "tekst_" + failinimi

    else:
        continue  # see fail ei vaja muutmist, jätame vahele

    vana_tee = os.path.join(kaust, failinimi)
    uus_tee  = os.path.join(kaust, uus_nimi)
    os.rename(vana_tee, uus_tee)
    print(f"  {failinimi}  →  {uus_nimi}")

print("Muudan failinimed väiketähtedeks ja lisan tänase kuupäeva...")
print("-" * 35)

tana = date.today().isoformat()

for failinimi in os.listdir(kaust):
    vana_tee = os.path.join(kaust, failinimi)

    if not os.path.isfile(vana_tee):
        continue

    vaike_nimi = failinimi.lower()  # muudab kogu nime väiketähtedeks

    if vaike_nimi.startswith(f"{tana}_"):
        uus_nimi = vaike_nimi
    else:
        uus_nimi = f"{tana}_{vaike_nimi}"  # lisab kuupäeva failinime ette

    if uus_nimi == failinimi:
        continue

    uus_tee = os.path.join(kaust, uus_nimi)
    os.rename(vana_tee, uus_tee)
    print(f"  {failinimi}  →  {uus_nimi}")

print("Failid pärast ümbernimetamist:")
print("-" * 35)
for failinimi in sorted(os.listdir(kaust)):
    print(failinimi)