import os  # os-moodul võimaldab failide ja kaustadega töötada

kaust = "failide-harjutus"  # kaust, milles tegutseme

print("Failid enne ümbernimetamist:")
print("-" * 35)

failid = os.listdir(kaust)   # tagastab nimekirja kaustas olevatest failidest
for failinimi in failid:
    print(failinimi)