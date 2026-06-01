# Süsteemi inventuur

Skript kogub arvuti kohta süsteemiinfot (OS, CPU, RAM, kettad, võrk) ning salvestab need JSON-formaadis faili.
Lisaks prinditakse konsoolile ka kokkuvõte.

---

## Kasutatud tehnoloogiad

- Python 3
- moodulid:
  - platform
  - psutil
  - socket
  - json
  - argparse


## Paigaldamine

Vaja paigaldada, pole Pythoniga kaasas:

```bash
pip install -r requirements.txt