# Git – 5-minutiline harjutus

Tee iga samm oma terminalis järjest. Harjutus katab git-i põhilise töövoo algusest lõpuni.

---

## Samm 1 – Seo end git-iga

> Ühekordsed seaded

```bash
git config --global user.name "Sinu Nimi"
git config --global user.email "sinu@email.com"
```

Git tahab teada, kes muudatusi teeb. See salvestatakse globaalselt — ei pea igas projektis kordama.

---

## Samm 2 – Loo uus repositoorium

> Projekti alustamine

```bash
mkdir minu-projekt && cd minu-projekt && git init
```

Loob uue kausta ja initsaliseerib seal git-i jälgimise. Pärast seda on kaustas peidetud `.git`-kaust.

---

## Samm 3 – Lisa fail ja vaata staatust

> Muudatuste jälgimine

```bash
echo "Tere, git!" > README.md
git status
```

`git status` näitab, millised failid on muutunud. Punane = jälgimata, roheline = lisatud lavastusalasse.

---

## Samm 4 – Lavasta muudatused (staging)

> Staging area

```bash
git add README.md
```

`git add` lisab faili lavastusalasse — see on nagu "valmistun seda salvestama". Kõikide failide jaoks: `git add .`

---

## Samm 5 – Loo commit (hetktõmmis)

> Salvestamine

```bash
git commit -m "Esimene commit: lisasin README"
```

Commit salvestab lavastusala hetktõmmise koos sõnumiga. `-m` tähistab commit message'it — kirjuta lühidalt, mida tegid.

---

## Samm 6 – Vaata ajalugu

> Ajaloo uurimine

```bash
git log --oneline
```

Näitab kõiki commiteid lühidalt. Iga commit saab unikaalse räsi (nt `a3f2c1b`). Täisajaloo nägemiseks: `git log`

---

## Samm 7 – Loo haru ja liitu tagasi

> Harud (branching)

```bash
git checkout -b uus-funktsioon
echo "uus rida" >> README.md
git add . && git commit -m "Lisasin uue rea"
git checkout main
git merge uus-funktsioon
```

Haru lubab katsetada ilma põhikoodi rikkumata. `git checkout -b` loob ja lülitab harusse. `git merge` ühendab tagasi.

---

*Harjutus kaetud käsud: `git config`, `git init`, `git status`, `git add`, `git commit`, `git log`, `git checkout`, `git merge`*