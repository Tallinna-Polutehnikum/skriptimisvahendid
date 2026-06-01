# Ülesanne D – Süsteemi inventuur

## Käivitamine

```bash
python3 inventuur.py
```

## Sõltuvused

- psutil

Paigaldamine:

```bash
sudo apt install python3-psutil
```

## Tulemus

Skript kogub süsteemi andmed ja salvestab need faili `inventuur.json`.

Kogutavad andmed:

- operatsioonisüsteem
- protsessor
- RAM
- kettaruum
- Pythoni versioon