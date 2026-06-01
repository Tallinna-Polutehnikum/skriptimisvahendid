# Süsteemi inventuur (Ülesanne D)

## Kirjeldus

See skript kogub arvuti süsteemi infot ja salvestab selle struktureeritud JSON faili.
Skript töötab Windows, Linux ja macOS operatsioonisüsteemides.

## Funktsionaalsus

Skript kogub järgmise info:

* Hosti nimi ja kasutaja
* Operatsioonisüsteemi info
* Python versioon
* CPU info (mudel, tuumade arv, kasutus)
* RAM kasutus
* Kettad (maht, vaba ruum, kasutus)
* Võrgukaardid ja nende IP-aadressid

## Käivitamine

```bash
python inventuur.py
```

## Parameetrid

* `--väljund <fail>` — määrab väljundfaili nime
  Näide:

  ```bash
  python inventuur.py --väljund minu_fail.json
  ```

* `--stdout` — prindib JSON väljundi konsooli

  ```bash
  python inventuur.py --stdout
  ```

## Väljund

Vaikimisi salvestatakse fail nimega:

```
inventuur_<hostname>_<kuupäev>.json
```

Näide:

```
inventuur_DESKTOP-2U1CKPO_2026-04-25.json
```

## Sõltuvused

Skript kasutab teeki **psutil**, mis tuleb eelnevalt paigaldada:

```bash
pip install psutil
```

## Testitud keskkond

* Windows 10
* Python 3.11

## Märkused

* Mõned võrgukaardid võivad olla virtuaalsed (nt VPN, Bluetooth)
* IP-aadressid kujul `169.254.x.x` tähendavad, et võrguühendus ei ole täielikult seadistatud
* CPU nimi võib erineda sõltuvalt operatsioonisüsteemist

## Kokkuvõte

Skript võimaldab kiiresti saada ülevaate arvuti süsteemi seisust ja salvestada selle JSON formaadis edasiseks analüüsiks.
