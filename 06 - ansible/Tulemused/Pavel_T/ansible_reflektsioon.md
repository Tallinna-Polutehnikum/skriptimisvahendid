# Ansible reflektsioon

## A osa

### A1.1

Minu arusaamise järgi aitab Ansible automatiseerida selliseid tegevusi, mida peaks muidu käsitsi paljudes serverites tegema. Näiteks programmide paigaldamine, seadistuste muutmine või teenuste käivitamine.

### A1.2

Peamine erinevus on see, et tavaline Bashi või Pythoni skript töötab tavaliselt ühes masinas, aga Ansible võimaldab hallata korraga paljusid servereid. Lisaks keskendub Ansible rohkem sellele, milline peab lõpptulemus olema, mitte ainult käskude järjestusele.

### A2.1

Control node on arvuti, kust Ansible käske käivitatakse. Managed node on server või seade, mida hallatakse. Minu puhul võiks control node olla minu Ubuntu WSL keskkond ja managed node näiteks mõni Linuxi server või virtuaalmasin.

### A2.2

Esimene käsk, mida näidati, oli Ansible ping. Selle eesmärk on kontrollida, kas Ansible saab hallatavate masinatega ühendust ja kas need vastavad.

### A2.3

Linuxi sihtmasinasse ei ole tavaliselt vaja eraldi agenti paigaldada. Ansible kasutab SSH ühendust ning vajab sihtmasinas Pythonit.

---

### A3.1

Inventory on fail või nimekiri, kus on kirjas kõik serverid, mida Ansible haldab. Selle põhjal teab Ansible, kuhu käske saata.

### A3.2

Inventory võib olla näiteks:

* INI formaadis
* YAML formaadis

### A3.3

Grupid on kasulikud selleks, et erinevaid servereid eraldi hallata. Näiteks võib olla grupp veebiserveritele ja teine andmebaasiserveritele. Siis saab nginxi paigaldada ainult veebiserveritele.

---

### A4.1

Playbookid on kirjutatud YAML formaadis. See on minu arvates lihtsamini loetav kui Python või Bash, sest seal kirjeldatakse rohkem soovitud tulemust kui programmi loogikat.

### A4.2

Task on üks konkreetne tegevus playbookis. Näiteks paketi paigaldamine, faili kopeerimine või teenuse käivitamine.

### A4.3

`hosts` määrab, milliste serverite peal playbook töötab. `become` tähendab, et ülesandeid täidetakse kõrgemate õigustega, näiteks root kasutajana.

---

### A5.1

| Mõiste       | Mida see tähendab?                          |
| ------------ | ------------------------------------------- |
| Control node | Arvuti, kust Ansible käivitatakse.          |
| Managed node | Server või seade, mida Ansible haldab.      |
| Inventory    | Hallatavate serverite nimekiri.             |
| Playbook     | YAML fail automaatsete tegevustega.         |
| Play         | Ülesannete kogum kindlate hostide jaoks.    |
| Task         | Üks konkreetne tegevus playbookis.          |
| Module       | Ansible tööriist mingi tegevuse tegemiseks. |
| Handler      | Task, mis käivitub ainult vajadusel.        |
| Collection   | Moodulite ja lisade kogumik.                |

### A5.2

Module teeb konkreetse töö ära, näiteks paigaldab paketi või kopeerib faili. Plugin laiendab Ansible võimalusi ja aitab selle tööd kohandada.

### A5.3

Task käivitatakse playbooki töö käigus alati. Handler käivitatakse ainult siis, kui mõni task selle välja kutsub.

---

## B osa

### B1

Kui peaksin seda tegema Bashi skriptiga, siis ühenduksin tõenäoliselt SSH kaudu igasse serverisse ja käivitaksin vajalikud käsud. Probleem tekib siis, kui mõni server on maas või ühendus katkeb. Sellisel juhul võivad mõned serverid saada seadistatud ja mõned mitte.

### B2

Ansible teeb sama asja palju mugavamalt. Kõik serverid on ühes inventory failis ja Ansible näitab kohe, millistel serveritel tegevus õnnestus ja millistel mitte. Samuti saab sama playbooki hiljem uuesti käivitada.

### B3

Minu arvates võiks Ansible sobida näiteks serverite kontrollimise või tarkvara paigaldamise ülesannete jaoks. Viimase nädala harjutused olid pigem lokaalsed skriptid, aga kui sama asja peaks tegema paljudes masinates, oleks Ansible kasulikum.

### B4

Idempotentsus tähendab seda, et sama tegevust võib mitu korda käivitada ja lõpptulemus jääb ikka samaks.

---

## C osa

### C1

See playbook töötab hostide grupi `veebid` peal. Seda näeb reast:

`hosts: veebid`

### C2

`vars` osa võimaldab väärtusi ühes kohas hoida. Nii ei pea sama teksti või paketi nime mitmes kohas eraldi kirjutama.

### C3

`inventory_hostname` asendatakse selle serveri nimega, mille peal playbook parajasti töötab. Kui kasutada servereid web1, web2 ja web3, siis avalehe tekst tuleb igal serveril erinev.

### C4

Task viitab handlerile käsuga `notify`. Handler ise käivitatakse ainult siis, kui mingi muudatus tegelikult toimus.

### C5

Teisel käivitamisel kontrollib Ansible süsteemi seisundit uuesti. Kui kõik on juba õigesti seadistatud, siis tavaliselt midagi ei muudeta ja väljundis on näha, et muudatusi ei tehtud.

---

## D osa

### D1

Kõige segasem osa oli alguses erinevate mõistete eristamine. Play, task, module ja handler tundusid algul üsna sarnased ning pidin mitu korda näiteid vaatama.

### D2

Mind üllatas see, et Ansible ei vaja Linuxi serverites eraldi agenti. Olin arvanud, et midagi tuleb kindlasti igasse masinasse paigaldada.

### D3

Tulevikus süsteemiadministraatorina võiks Ansible olla kasulik serverite seadistamisel, tarkvara paigaldamisel ja uuenduste tegemisel. Eriti siis, kui hallata tuleb rohkem kui paari serverit.

### D4

Kui ettevõttes on sadu või isegi tuhandeid servereid, siis kuidas inventory failid tavaliselt organiseeritakse, et neid oleks lihtne hallata ja ajakohasena hoida?
