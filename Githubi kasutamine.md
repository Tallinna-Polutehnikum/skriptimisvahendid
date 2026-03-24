# GitHub – kasutuselevõtu juhend

GitHub on veebipõhine platvorm git-repositooriumide majutamiseks ja meeskonnatööks. See juhend eeldab, et git on juba arvutis seadistatud (vt `git-harjutus.md`).

---

## Samm 1 – Loo GitHub konto

> Registreerimine

Mine aadressile [github.com](https://github.com) ja loo tasuta konto. Kasuta sama e-posti, mille seadsid git-i konfiguratsiooniks:

```bash
git config --global user.email  # vaata, mis e-post on seatud
```

---

## Samm 2 – Seadista SSH võti

> Turvaline ühendus

SSH võti võimaldab githubiga suhelda ilma parooli sisestamata.

```bash
ssh-keygen -t ed25519 -C "sinu@email.com"
```

Vajuta enter kõigile küsimustele (vaikeväärtused sobivad). Seejärel kopeeri avalik võti:

```bash
cat ~/.ssh/id_ed25519.pub
```

Mine GitHubis **Settings → SSH and GPG keys → New SSH key**, kleebi sisu ja salvesta.

Testi ühendust:

```bash
ssh -T git@github.com
```

Edukas vastus: `Hi kasutajanimi! You've successfully authenticated...`

---

## Samm 3 – Loo uus repositoorium GitHubis

> Remote repo loomine

Mine [github.com/new](https://github.com/new) ja täida:

- **Repository name:** `minu-projekt`
- **Visibility:** Public või Private
- Jäta "Initialize with README" **märkimata** (lisame ise)

Klõpsa **Create repository**.

---

## Samm 4 – Ühenda lokaalne repo GitHubiga

> Remote lisamine

Kopeeri GitHubi lehelt SSH URL (kujul `git@github.com:kasutajanimi/minu-projekt.git`) ja käivita:

```bash
cd minu-projekt
git remote add origin git@github.com:kasutajanimi/minu-projekt.git
git branch -M main
git push -u origin main
```

`-u` seob lokaalse `main`-haru remote'i `main`-haruga — edaspidi piisab lihtsalt `git push`.

---

## Samm 5 – Igapäevane töövoog

> Push ja pull

Pärast muudatuste tegemist ja commitimist saada need GitHubi:

```bash
git push
```

Kui keegi teine on repo muutnud (või töötad mitmes arvutis), tõmba muudatused alla:

```bash
git pull
```

---

## Samm 6 – Klooni olemasolev repositoorium

> Repo kopeerimine

Kellegi teise (või enda) repo allalaadimiseks:

```bash
git clone git@github.com:kasutajanimi/repo-nimi.git
```

See loob lokaalse koopia koos kogu ajalooga ja seab remote'i automaatselt.

---

## Samm 7 – Loo Pull Request

> Koodiülevaatus meeskonnas

Pull Request (PR) on viis pakutud muudatusi üle vaadata enne põhiharusse liitmist.

```bash
git checkout -b minu-funktsioon
# tee muudatusi...
git add . && git commit -m "Lisa uus funktsioon"
git push -u origin minu-funktsioon
```

Seejärel mine GitHubis repole — ilmub teade **"Compare & pull request"**. Klõpsa sellel, lisa kirjeldus ja loo PR. Tiimikaaslased saavad kommenteerida ja kinnitada enne liitmist.

---

## Kasulikud GitHub funktsioonid

| Funktsioon | Kirjeldus |
|---|---|
| **Issues** | Vigade ja ülesannete jälgimine |
| **Actions** | Automaatne testimine ja deploy |
| **Wiki** | Projektidokumentatsioon |
| **Releases** | Versioonide publitseerimine |
| **Fork** | Teise repo kopeerimine oma kontole muutmiseks |

---

*Kaetud käsud: `git remote`, `git push`, `git pull`, `git clone`, `ssh-keygen`*