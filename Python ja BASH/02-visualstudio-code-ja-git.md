**Skriptimise alustamine Visual Studio Code-is**

**Git ja GitHubi alustamine**

Git on versioonihaldussüsteem, mis võimaldab teil jälgida oma koodi muudatusi. GitHub on veebiplatvorm, mis võimaldab teil oma Git-hoidlaid hoida ja jagada.

**Git ja GitHubi alustamiseks järgige neid samme:**

1. **Looge GitHubi konto.**
2. **Looge uus repositoorium.**
3. **Kloonige repositoorium oma arvutisse.**
4. **Seadke sisse GitHubi autentimine Visual Studio Code-is.**

**1. Looge GitHubi konto**

Avage veebibrauser ja minge aadressile https://github.com/. Klõpsake nuppu "Registreeru" ja järgige ekraanil kuvatavaid juhiseid.

**2. Looge uus repositoorium**

Pärast GitHubi konto loomist minge oma konto lehele. Klõpsake nuppu "Loo uus repositoorium".

Repositoooriumi nimeks saate panna näiteks "minu_esimene_projekt". Valige "Private" režiim, kui soovite, et repositoorium oleks privaatne.

**3. Kloonige repositoorium oma arvutisse**

Kui olete repositooriumi loonud, saate selle kloonida oma arvutisse. Kloonimine loob koopia repositooriumist teie arvutisse.

Avage käsurea ja navigeerige kausta, kuhu soovite repositooriumi kloonida. Seejärel käivitage järgmine käsk:

```
git clone https://github.com/[teie_kasutajanimi]/[repositooriumi_nimi].git
```

Näiteks kui teie GitHubi kasutajanimi on "bard" ja repositooriumi nimi on "minu_esimene_projekt", siis käivitage järgmine käsk:

```
git clone https://github.com/bard/minu_esimene_projekt.git
```

**4. Seadke sisse GitHubi autentimine Visual Studio Code-is**

Visual Studio Code võimaldab teil kasutada GitHubi autentimist, et pääseda juurde oma GitHubi kontole ja repositooriumitele.

Avage Visual Studio Code ja minge menüüribale "Tööriistad" > "GitHub" > "Seadista GitHubi autentimine".

Järgige ekraanil kuvatavaid juhiseid.

**5. Ava repo Visual Studio Codes**

Pärast GitHubi autentimise seadistamist saate avada oma repositooriumi Visual Studio Codes.

Avage Visual Studio Code ja minge menüüribale "Fail" > "Ava".

Valige oma repositooriumi kaust ja klõpsake nuppu "Ava".

**6. Proovige luua oma esimene programm**

Nüüd, kui olete oma repositooriumi Visual Studio Codes avanud, saate hakata kirjutama oma esimest programmi.

Looge uus Pythoni fail ja salvestage see nimega "tere_maailm.py". Seejärel lisage faili järgmine kood:

```python
print("Tere, maailm!")
```

Salvestage fail ja käivitage see, vajutades klahvikombinatsiooni `F5`.

**7. Tee Visual Studio Code abil commit ja push (sync)**

Kui olete oma programmi salvestanud, saate teha commiti, et salvestada oma muudatused repositooriumisse.

Visual Studio Codes saate teha commiti, vajutades klahvikombinatsiooni `Ctrl`+`Shift`+`K`.

Seejärel sisestage commiti sõnum ja klõpsake nuppu "Commit".

Lõpuks saate oma muudatused pushida GitHubi, et teised saaksid neid vaadata.

Visual Studio Codes saate oma muudatused pushida GitHubi, vajutades klahvikombinatsiooni `Ctrl`+`Shift`+`P` ja sisestades "Push".

Seejärel sisestage oma GitHubi kasutajanimi ja parool ning klõpsake nuppu "Push".

**Materjal Git ja GitHubiga alustamiseks**

**Git**

* **Giti põhitõed:** https://git-scm.com/book
