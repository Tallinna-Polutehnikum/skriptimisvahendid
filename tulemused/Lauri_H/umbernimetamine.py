import os  # os-moodul võimaldab failide ja kaustadega töötada

kaust = "failide-harjutus"  # kaust, milles tegutseme

print("Failid pärast ümbernimetamist:")
print("-" * 35)
for failinimi in sorted(os.listdir(kaust)):
    print(failinimi)
