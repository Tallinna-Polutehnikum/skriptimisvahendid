import os  # os-moodul võimaldab failide ja kaustadega töötada

kaust = "failide-harjutus"  # kaust, milles tegutseme

print("Failid enne ümbernimetamist:")
print("-" * 35)

failid = os.listdir(kaust)   # tagastab nimekirja kaustas olevatest failidest
for failinimi in failid:
    print(failinimi)

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

print("Failid pärast ümbernimetamist:")
print("-" * 35)
for failinimi in sorted(os.listdir(kaust)):
    print(failinimi)