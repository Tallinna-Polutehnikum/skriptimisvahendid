# Serverite saadavuse monitor (Ülesanne B)

## Kirjeldus

PowerShell skript, mis kontrollib serverite/hostide kättesaadavust.

Skript:

* loeb hostide nimekirja CSV-failist
* kontrollib ühendust (ping või TCP port)
* kuvab tulemuse konsoolis
* salvestab tulemuse CSV-faili

---

## ▶Käivitamine

```powershell
.\kontrolli-hostid.ps1
```

---

## Sisendfail

Fail:

```text
hostid.csv
```

Näide:

```csv
nimi,host,port,kirjeldus
google,google.com,443,Avalik võrgutest
```

---

## Väljund

### Konsool

* iga hosti staatus (OK / FAIL)
* viivitus ms
* kokkuvõte

### CSV

Fail:

```text
saadavus_<kuupäev>.csv
```

Sisaldab:

* host
* olek
* viivitus
* kontrollimise aeg

---

## Kasutatud käsud

* Test-Connection
* Test-NetConnection
* Import-Csv
* Export-Csv

---

## Märkused

* Skript ei katke ühe hosti vea korral
* FAIL hostid käsitletakse eraldi
* TCP kontroll kasutatakse, kui port on määratud

---

## Disainiotsused

* Kasutatud funktsioon `Test-HostStatus`
* try/catch tagab töökindluse
* CSV väljund võimaldab edasist analüüsi
* Konsooliväljund vormindatud tabelina

---
