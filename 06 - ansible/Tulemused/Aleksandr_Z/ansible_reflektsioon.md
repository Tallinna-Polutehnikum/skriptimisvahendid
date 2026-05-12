# Ansible reflektsioon — Aleksandr Z

## A osa — lugemine ja kontrollküsimused

### A1.1
Ansible automatiseerib serverite ja süsteemide haldamist. Sellega saab korraga paigaldada programme, muuta konfiguratsioone ja käivitada käske paljudes arvutites.

### A1.2
Tavaline skript käivitab käsud järjest ja peab ise kontrollima vigu. Ansible kasutab valmis mooduleid ja kontrollib süsteemi seisundit automaatselt.

---

### A2.1
Control node on arvuti, kust Ansible käivitatakse. Managed node on sihtarvuti või server, mida Ansible haldab. Minu arvutis võiks control node olla minu Windows/Linux masin ja managed node näiteks virtuaalserver.

### A2.2
Esimene käsk oli:

```bash
ansible all -m ping
```

See kontrollib, kas ühendus sihtmasinatega töötab.

### A2.3
Ansible ei vaja sihtmasinas eraldi agenti. Tavaliselt piisab SSH ühendusest ja Pythonist Linuxi serveris.

---

### A3.1
Inventory on fail või nimekiri, kus on kirjas kõik serverid ja seadmed, mida Ansible haldab. Seal saab servereid grupeerida ja neile seadistusi määrata.

### A3.2
Inventory võib olla näiteks:
- INI formaat
- YAML formaat

### A3.3
Grupid aitavad hallata erinevaid servereid eraldi. Näiteks saab veebiserveritele paigaldada nginx ja andmebaasiserveritele PostgreSQL.

---

### A4.1
Playbookid on kirjutatud YAML formaadis. See erineb Pythonist ja Bashist, sest seal kirjeldatakse soovitud tulemust, mitte samm-sammult programmeerimisloogikat.

### A4.2
Task on üks tegevus playbookis, näiteks paketi paigaldamine või faili kopeerimine.

### A4.3
`hosts:` näitab, milliste serverite peal playbook töötab.  
`become:` tähendab, et käsud käivitatakse administraatori õigustes.

---

## A5

| Mõiste | Mida see tähendab? |
|---|---|
| Control node | Arvuti, kust Ansible töötab |
| Managed node | Server või arvuti, mida hallatakse |
| Inventory | Serverite nimekiri |
| Playbook | YAML fail automatiseerimise jaoks |
| Play | Grupp tegevusi kindlate serverite jaoks |
| Task | Üks konkreetne tegevus |
| Module | Valmis tööriist mingi ülesande tegemiseks |
| Handler | Task, mis käivitub ainult vajadusel |
| Collection | Moodulite ja pluginate kogum |

### A5.1
Module teeb konkreetset tööd, näiteks paigaldab paketi. Plugin laiendab Ansible funktsionaalsust.

### A5.2
Task käivitatakse alati playbooki jooksul. Handler käivitub ainult siis, kui mingi task sellest teada annab.

---

# B osa — seos varasemate teadmistega

### B1
Bashi skriptiga peaks kasutama tsüklit ja SSH ühendusi kõigi serverite jaoks. Kui üks server katkeb või install läheb pooleli, siis võib süsteem jääda ebastabiilsesse olekusse.

### B2
Ansible kontrollib serverite seisundit automaatselt ja teeb muudatusi ainult vajadusel. Samuti näitab see täpselt, milline server ebaõnnestus.

### B3
Notifikatsioonimooduli või logide kontrollimise ülesanded võiksid sobida Ansible jaoks. Seda oleks lihtsam korraga paljudes serverites kasutada.

### B4
Idempotentsus tähendab, et sama tegevuse mitu korda käivitamine ei muuda süsteemi uuesti ega tekita vigu.

---

# C osa — playbooki analüüs

### C1
Playbook töötab grupi `veebid` serverite peal. Seda näeb real:

```yaml
hosts: veebid
```

### C2
`vars:` osa hoiab muutujaid ühes kohas. Nii on lihtsam hiljem väärtusi muuta ja playbook jääb loetavamaks.

### C3
`{{ inventory_hostname }}` asendatakse serveri nimega.  
Kui serverid on web1, web2 ja web3, siis avalehed on erinevad.

### C4
Task `Restart nginx` ainult saadab handlerile teavituse. Handler käivitub alles siis, kui fail või konfiguratsioon muutus.

### C5
Teisel käivitamisel midagi uut ei muudeta, sest süsteem on juba õiges seisundis. Väljund näitab enamasti `ok`, mitte `changed`.

---

# D osa — reflektsioon

### D1
Kõige keerulisem oli alguses aru saada inventory ja playbookide seosest.

### D2
Huvitav oli see, et Ansible ei vaja agenti sihtserveris ja kasutab lihtsalt SSH ühendust.

### D3
Ansible võiks olla kasulik serverite automaatseks seadistamiseks ja tarkvara paigaldamiseks ettevõtte võrgus.

### D4
Kuidas kasutatakse Ansible'it suurtes ettevõtetes koos Dockeri ja Kubernetesega?
