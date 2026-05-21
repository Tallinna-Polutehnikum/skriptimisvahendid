## A osa — lugemine ja kontrollküsimused

### 1. [Introduction to Ansible](https://docs.ansible.com/projects/ansible/latest/getting_started/introduction.html)

- **A1.1** Mida Ansible **automatiseerib**? Kirjuta 1–2 lauset oma sõnadega.
Ansible automatiseerib skriptide jooksutamist ja tarkvara deployimist.

- **A1.2** Mis on sinu arust põhiline erinevus Ansible'i ja tavalise skripti (Bash, Python) vahel?
Ansible kirjeldab pigem seadme lõpptulemust, tavaline skript jookseb ilma lõpptulemust kontrollimata (kui pole seda skripti sisse pandud).

### 2. [Start automating with Ansible](https://docs.ansible.com/projects/ansible/latest/getting_started/get_started_ansible.html)

- **A2.1** Mis on **control node** ja mis on **managed node**? Kirjelda, kus need sinu enda arvutis võiksid olla.
Control node on seade, mille peal Ansible jookseb. Managed node on seade, mida control node seadmega hallata saab. Kodukeskkonnas **saaks** control node olla isiklik arvuti ja managed node olla ruuter.

- **A2.2** Milline oli esimene Ansible-käsk, mida materjalis näitati? Mida see käsk teeb?
Esimesena näidati `pip install ansible`, see installeerib Ansible arvutisse, kus saab automatiseerimist hakata ehitama.

- **A2.3** Kas Ansible nõuab sihtmasinas mingit eritarkvara installimist? Põhjenda.
Ei vaja, kuna ühendus hallatavate seadmetega toimib olemasolevate protokollide kaudu nt SSH.

### 3. [Building an inventory](https://docs.ansible.com/projects/ansible/latest/getting_started/get_started_inventory.html)

- **A3.1** Mis on **inventory**? Tee kahe lausega selgitus.
Inventory on fail/list, kus kirjas seadmed mida control node haldab. Kirjas on ka nende ühendusinfo ja grupid.

- **A3.2** Millistes formaatides võib inventory olla? Nimeta vähemalt kaks.
Inventory võib olla nii INI kui ka YAML formaatides.

- **A3.3** Miks on grupid (`[veebiserverid]`, `[andmebaasid]` jne) inventory's kasulikud? Too näide olukorrast, kus see vahet teeks.
Grupid on kasulikud, kuna siis saab käsu saata mitmele seadmele korraga, ei pea eraldi haldama seadmeid. Näiteks kui 100-le seadmele on vaja korraga paigaldada tarkvara, saab need grupeerida ja paigaldada tarkvara tervele grupile.

### 4. [Creating a playbook](https://docs.ansible.com/projects/ansible/latest/getting_started/get_started_playbook.html)

- **A4.1** Mis keeles (formaadis) on playbook'id kirjutatud? Mille poolest see formaat erineb Pythonist või Bashist?
YAML formaadis, see on lihtsam ja loetavam keel, info on kiiresti kättesaadav.

- **A4.2** Mis on **task** playbook'is?
Task on üks konkreetne tegevus, mida Ansible peab tegema.

- **A4.3** Vaata näiteplaybook'i materjalis. Mida tähendab seal `hosts:`? Mida tähendab `become:`?
`hosts:` tähendab milliste seadmete peal see playbook käivitatakse. `become:` tähendab kas kasutada root õigusi või mitte.

### 5. [Ansible concepts](https://docs.ansible.com/projects/ansible/latest/getting_started/basic_concepts.html)

See on kõige tihedam alaleht. Loe läbi, siis täida tabel **oma sõnadega** (mitte koopia dokumentatsioonist):

| Mõiste | Mida see tähendab? (1 lause) |
|---|---|
| Control node | Seade, kust Ansible käske käivitatakse. |
| Managed node | Hallatav seade, mida Ansible seadistab. |
| Inventory | Fail/nimekiri seadmetest, mida Ansible haldab. |
| Playbook | YAML formaadis fail, mis kirjeldab, mida Ansible tegema peab. |
| Play | Osa Playbookist, seob taskid ja hostid. |
| Task | Üks kindel tegevus. |
| Module | Koodiosa, mis teeb taski. |
| Handler | Task, mis käivitub ainult siis, kui seda vajatakse. |
| Collection | Paketid moodulitest ja pluginatest. |

- **A5.1** Mille poolest erineb **module** ja **plugin**?
Module reaalselt ka käivitab midagi. Plugin laiendab Ansible funktsionaalsust kas control või managed node peal.

- **A5.2** Mille poolest erineb **task** ja **handler**?
Task jookseb alati, handler jookseb kui seda kutsutakse. 

---

## B osa — seos sellega, mida juba tead

Sa oled juba kirjutanud Pythoni, PowerShelli ja Bashi skripte. Mõtle nüüd Ansible'i peale selle taustal.

- **B1** Sul on 30 serverit, igaühele tuleb paigaldada nginx ja luua sama konfifail. Kuidas teeksid seda **Bashi** skriptiga? Mis läheb halvasti, kui üks server vahepeal alla kukub või paigaldus jookseb pooleldi läbi?
Arvatavasti ühenduks skripti sees serveritega SSH kaudu vms, paigaldaks nginx-i ühekaupa läbi skripti nende peale. Sellise skriptiga pole teada kus täpselt paigaldamine pooleli jäi, ehk peaks kõik serverid üle kontrollima, kas neil tarkvara olemas.

- **B2** Kuidas Ansible sama ülesannet teisiti lahendab? Mis muutub?
Jooksutades ühe playbooki ja grupeerides kõik serverid korraga, jooksutab ta käsu kõigi peal korraga. Kontrollitavus ja stabiilsus muutub.


- **B3** Vaata viimase nädala harjutusi (notifikatsioonimoodul, suurimad failid jne). Kas mõni sealne ülesanne sobiks Ansible'i kasutuseks paremini kui skriptiga? Põhjenda.
ID tarkvara uuenduse kontroll sobiks hästi, kuna see juba ehitati saatma väliseid teateid, mida oleks lihtne kohe vaadata ja kasutajat sellest teavitada.


- **B4** Sõnasta **idempotentsus** ühes lauses oma sõnadega. *(Vihje: mõelge `apt install nginx` peale — mis juhtub teisel käivitamisel skriptiga ja mis Ansible'iga?)*
Sama asja mitu korda käivitades jääb tulemus samaks, duplikeerimist pole.

---

## C osa — loe ja seleta seda playbook'i

Vasta:

- **C1** Kelle peal see playbook töötab? Kust seda näed?
Playbook töötab grupi `veebid` peal. Näeb realt `hosts:veebid`.

- **C2** Mis on `vars:` osa funktsioon? Miks ei kirjutatud `nginx` ja avalehe tekst kohe taskidesse?
`vars:` osa määrab muutujad, mida saab ka hiljem taskides kasutada. `nginx` ja avalehe tekst on kasulikum hoida muutujates, siis saab muuta nt avalehe teksti ühes kohas, mitte kõigis eraldi.

- **C3** Mida teeb `{{ inventory_hostname }}`? Kui playbook käivitatakse kolme serveri peal (web1, web2, web3), kas avalehed on samad või erinevad?
`{{ inventory_hostname }}` asendatakse hosti nimega, avalehed on erinevad hostinime poolest.

- **C4** Mis vahe on **task**-il "Restart nginx" ja **handler**-il "Restart nginx"? Millal handler käivitub?
Handler käivitub `notify: Restart nginx` kaudu, käivitub alles siis, kui avalehe sisu on muutunud. Task sisumuutust ei kontrolliks.

- **C5** Kui käivitad selle playbook'i kaks korda järjest, mis juhtub teisel käivitamisel? Mida väljund näitab?
Ei peaks midagi juhtuma, väljund peaks näitama et kõik on paigaldatud õigesti ja teine käivitus ei muuda midagi.

---

## D osa — avatud reflektsioon

Need küsimused on subjektiivsed — õigeid vastuseid pole. Kirjuta lühike, aus vastus.

- **D1** Mis oli kõige **arusaamatum** koht materjalis? *(Kui kõik oli selge, siis tunnista seda julgelt — aga ole enda vastu aus.)*
Materjal oli suhteliselt arusaadav, kuigi pidi edasi-tagasi kerima et termineid paremini endale selgeks teha. 

- **D2** Mis tundus **üllatav** või huvitav?
Pani mõtlema, miks seda laialdasemalt töökohas kasutuses pole ja mis võimalused enda töö lihtsustamiseks see võimaldab.

- **D3** Kus **sinu enda igapäevatöös** (või tulevases töös IT-administraatorina) võiks Ansible kasulik olla?
Onboardingul seadmete seadistus.

- **D4** **Üks küsimus**, mille tahad arutelu ajal teistega või õpetajaga läbi rääkida. *(Pane see kindlasti — see on aluseks meie 12.00 algavale arutlusele.)*
Kus te ise Ansible-t kasutate/mis eesmärkideks?
---