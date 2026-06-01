# Logianalüüsi skript

## Kirjeldus

See skript loeb logifaili `ps-alerts.log` ja teeb sellest kokkuvõtte:

- mitu teadet kokku
- kui palju oli OK vs FAIL
- jaotus (Info / Warning / Critical)
- top allikad
- critical-teated päeva kaupa

Skript salvestab CSV faili, info päevade kaupa.

---

## Käivitamine

Vaikimisi
```bash
python analyysi_logi.py
``