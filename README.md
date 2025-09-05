# Python Kurz pro Základní Školy

Výuková platforma pro Python vytvořená s FastAPI, určená pro studenty základních škol.

## 🚀 Funkce

- **Interaktivní kurzy**: Úvod, Základy a Pokročilé koncepty Pythonu
- **Python Playground**: Spouštění Python kódu přímo v prohlížeči
- **Sledování pokroku**: Profil studenta s dokončenými lekcemi
- **Responzivní design**: Vhodný pro tablety i počítače
- **Dětský design**: Barevný a přátelský interface

## 📁 Struktura projektu

```
python-kurz/
├── main.py                 # Hlavní FastAPI aplikace
├── requirements.txt        # Python závislosti
├── README.md              # Tento soubor
├── templates/             # HTML šablony (Jinja2)
│   ├── base.html          # Základní šablona
│   ├── index.html         # Hlavní stránka
│   ├── kurz.html          # Stránka kurzu
│   ├── lekce.html         # Stránka lekce
│   ├── playground.html    # Python playground
│   └── profil.html        # Profil studenta
└── static/                # Statické soubory
    ├── css/
    │   └── style.css      # Hlavní styly
    └── js/
        └── main.js        # JavaScript funkce
```

## 🛠️ Instalace a spuštění

### Požadavky
- Python 3.8 nebo vyšší
- pip (správce balíčků Pythonu)

### Kroky instalace

1. **Naklonujte nebo stáhněte projekt**
   ```bash
   # Pokud máte git
   git clone <repository-url>
   cd python-kurz
   
   # Nebo jednoduše stáhněte a rozbalte soubory
   ```

2. **Vytvořte virtuální prostředí (doporučeno)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Nainstalujte závislosti**
   ```bash
   pip install -r requirements.txt
   ```

4. **Spusťte aplikaci**
   ```bash
   python main.py
   ```

5. **Otevřete prohlížeč**
   - Přejděte na: http://localhost:8000
   - Nebo: http://127.0.0.1:8000

## 📚 Použití

### Hlavní stránka
- Přehled všech dostupných kurzů
- Statistiky pokroku studenta
- Rychlé akce (Playground, Profil)

### Kurzy
- **Úvod do Pythonu**: Základní koncepty programování
- **Základy Pythonu**: Proměnné, podmínky, cykly
- **Pokročilé koncepty**: Funkce, seznamy, soubory

### Python Playground
- Interaktivní editor pro testování kódu
- Spouštění Python kódu na serveru
- Předpřipravené příklady
- Zobrazení výstupu a chyb

### Profil studenta
- Sledování dokončených lekcí
- Pokrok v jednotlivých kurzech
- Úspěchy a statistiky
- Nedávná aktivita

## 🎨 Design

Aplikace používá:
- **Bootstrap 5** pro responzivní layout
- **Font Awesome** pro ikony
- **Vlastní CSS** s dětským designem
- **Gradienty a animace** pro atraktivní vzhled
- **Responzivní design** pro všechna zařízení

## 🔧 Technické detaily

### Backend (FastAPI)
- **FastAPI**: Moderní webový framework
- **Jinja2**: Template engine pro HTML
- **Uvicorn**: ASGI server
- **Python subprocess**: Spouštění kódu

### Frontend
- **HTML5**: Sémantické značky
- **CSS3**: Flexbox, Grid, animace
- **JavaScript**: Interaktivní funkce
- **Bootstrap**: Responzivní komponenty

### Bezpečnost
- **Timeout**: Kód se spouští max 5 sekund
- **Sandbox**: Izolované spouštění kódu
- **Validace**: Kontrola vstupů

## 🚨 Omezení

- **Timeout**: Python kód má limit 5 sekund
- **Paměť**: Omezené prostředky pro spouštění kódu
- **Knihovny**: Pouze standardní Python knihovny
- **Soubory**: Žádný přístup k souborovému systému

## 🔮 Budoucí vylepšení

- [ ] Databáze pro trvalé ukládání pokroku
- [ ] Uživatelské účty a přihlašování
- [ ] Více programovacích jazyků
- [ ] Gamifikace (body, levely, odznaky)
- [ ] Chat nebo fórum pro studenty
- [ ] Pokročilé lekce s interaktivními cvičeními
- [ ] Export certifikátů
- [ ] Offline režim

## 🐛 Řešení problémů

### Aplikace se nespustí
- Zkontrolujte, zda máte Python 3.8+
- Ověřte instalaci závislostí: `pip install -r requirements.txt`
- Zkontrolujte, zda port 8000 není obsazený

### Kód se nespouští v Playground
- Zkontrolujte syntaxi Python kódu
- Ověřte, že nepoužíváte externí knihovny
- Zkuste jednodušší kód

### Problémy s designem
- Vymažte cache prohlížeče
- Zkontrolujte, zda se načítají CSS soubory
- Ověřte JavaScript konzoli pro chyby

## 📞 Podpora

Pro technickou podporu nebo dotazy:
- Zkontrolujte tento README
- Prohlédněte si kód v `main.py`
- Zkuste restartovat aplikaci

## 📄 Licence

Tento projekt je vytvořen pro vzdělávací účely. Můžete ho volně používat a upravovat.

---

**Vytvořeno s ❤️ pro výuku Pythonu na základních školách**
