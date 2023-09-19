# Harjutused
* Looge Pythoni funktsioon, mis liidab kaks arvu.
* Looge Pythoni funktsioon, mis tagastab arvude loendi summa.
* Looge Pythoni tsükkel, mis prindib ekraanile numbrid 1 kuni 10.
* Looge Pythoni tsükkel, mis prindib ekraanile paarisarvud 1 kuni 10.
* Looge Pythoni tsükkel, mis prindib ekraanile kõik arvud, mis jaguvad 3-ga.

# Esitamine
Näita järgmises tunnis iga probleemi lahendust eraldi Pythoni failist. Ole valmis küsimusteks ning failide muutmiseks. 


## Vihjed

**1. Looge Pythoni funktsioon, mis liidab kaks arvu.**

* Funktsioon peaks võtma kaks arvu argumendina.
* Funktsioon peaks tagastama nende arvude summa.
* Siin on näide funktsionaalsest koodist:

```python
def liitmine(x, y):
  """
  See funktsioon liidab kaks arvu.

  Args:
    x: Esimene arv.
    y: Teine arv.

  Returns:
    Summa.
  """

  return x + y

print(liitmine(1, 2))
```

**2. Looge Pythoni funktsioon, mis tagastab arvude loendi summa.**

* Funktsioon peaks võtma loendi arvudest argumendina.
* Funktsioon peaks tagastama loendi elementide summa.
* Siin on näide funktsionaalsest koodist:

```python
def summa(arvud):
  """
  See funktsioon tagastab arvude loendi summa.

  Args:
    arvud: Arvude loend.

  Returns:
    Summa.
  """

  summa = 0
  for arv in arvud:
    summa += arv
  return summa

arvud = [1, 2, 3]
print(summa(arvud))
```

**3. Looge Pythoni tsükkel, mis prindib ekraanile numbrid 1 kuni 10.**

* Tsükkel peaks korduma 10 korda.
* Iga korduse ajal peaks tsükkel printima ekraanile ühe numbri.
* Siin on näide tsüklilisest koodist:

```python
for i in range(1, 11):
  print(i)
```

**4. Looge Pythoni tsükkel, mis prindib ekraanile paarisarvud 1 kuni 10.**

* Tsükkel peaks korduma 10 korda.
* Iga korduse ajal peaks tsükkel kontrollima, kas number on paaris.
* Kui number on paaris, peaks tsükkel printima ekraanile selle.
* Siin on näide tsüklilisest koodist:

```python
for i in range(1, 11):
  if i % 2 == 0:
    print(i)
```

**5. Looge Pythoni tsükkel, mis prindib ekraanile kõik arvud, mis jaguvad 3-ga.**

* Tsükkel peaks korduma 10 korda.
* Iga korduse ajal peaks tsükkel kontrollima, kas number jagub 3-ga.
* Kui number jagub 3-ga, peaks tsükkel printima ekraanile selle.
* Siin on näide tsüklilisest koodist:

```python
for i in range(1, 11):
  if i % 3 == 0:
    print(i)
```
