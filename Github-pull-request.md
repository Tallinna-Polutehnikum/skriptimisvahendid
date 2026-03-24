# Juhend: kuidas lisada oma repo klassi nimekirja

Selles juhendis lisad oma GitHubi repositooriumi lingi faili `klassi-repod.md` Pull Requesti kaudu.

---

## Eeldused

- Sul on GitHubi konto
- Git on arvutis seadistatud (`git config --global user.name` ja `user.email`)
- Sul on olemas oma GitHubi repositoorium, mille linki lisad

---

## Samm 1 – Tee fork

Mine aadressile:
👉 [https://github.com/Tallinna-Polutehnikum/skriptimisvahendid](https://github.com/Tallinna-Polutehnikum/skriptimisvahendid)

Klõpsa lehe paremas ülanurgas nupul **Fork** → **Create fork**.

GitHub loob sinu kontole koopia repositooriumist.

---

## Samm 2 – Klooni fork oma arvutisse

Kopeeri oma fork'i SSH URL (kujul `git@github.com:SINUKASUTAJANIMI/skriptimisvahendid.git`) ja käivita terminalis:

```bash
git clone git@github.com:SINUKASUTAJANIMI/skriptimisvahendid.git
cd skriptimisvahendid
```

---

## Samm 3 – Loo uus haru

```bash
git checkout -b lisa-minu-repo
```

Ära tee muudatusi otse `main`-harusse — uus haru hoiab asjad korras.

---

## Samm 4 – Muuda faili `klassi-repod.md`

Ava fail tekstiredaktoris ja lisa oma rida olemasoleva nimekirja lõppu järgmises vormingus:

```markdown
- [Eesnimi P](https://github.com/sinukasutajanimi/sinu-repo-nimi)
```

**Näide:**

```markdown
- [Marko T](https://github.com/markot99/skriptid)
```

Asenda `Eesnimi` oma eesnimega ja `P` perekonnanime esitähega.  
Asenda link oma repositooriumi tegeliku aadressiga.

Salvesta fail.

---

## Samm 5 – Commit ja push

```bash
git add klassi-repod.md
git commit -m "Lisa Eesnimi P repo"
git push -u origin lisa-minu-repo
```

Asenda commit-sõnumis `Eesnimi P` oma nimega.

---

## Samm 6 – Ava Pull Request

1. Mine GitHubis oma fork'i lehele: `github.com/SINUKASUTAJANIMI/skriptimisvahendid`
2. Ilmub roheline teade **"Compare & pull request"** — klõpsa sellel
3. Kontrolli, et PR läheb õigesse kohta:
   - **base repository:** `Tallinna-Polutehnikum/skriptimisvahendid` → `main`
   - **head repository:** `SINUKASUTAJANIMI/skriptimisvahendid` → `lisa-minu-repo`
4. Pealkirjaks kirjuta: `Lisa Eesnimi P repo`
5. Klõpsa **Create pull request**

---

## Valmis! ✓

Õpetaja vaatab sinu PR üle ja liidab selle. Kui midagi on valesti, kommenteeritakse PR-i — paranda ja push uuesti samasse harusse, PR uuendub automaatselt.

---

### Levinud vead

| Viga | Lahendus |
|---|---|
| Push ebaõnnestub (`permission denied`) | Kontrolli, kas SSH võti on GitHubis lisatud |
| PR läheb valesse repo | Kontrolli PR avamisel `base repository` valikut |
| Nimi puudu või vale formaat | Veendu, et kasutad formaati `Eesnimi P` |
| Muutsin `main`-haru otse | Loo uus haru, kopeeri muudatus sinna |