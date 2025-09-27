# Python Kurz pro Základní Školy

Výuková platforma pro Python vytvořená s FastAPI, určená pro studenty základních škol.

## 🚀 Funkce

- **Interaktivní kurzy**: Úvod, Základy a Pokročilé koncepty Pythonu
- **Python Playground**: Spouštění Python kódu přímo v prohlížeči
- **Uživatelské účty**: Registrace, přihlášení a správa profilů
- **Sledování pokroku**: Individuální pokrok každého studenta
- **Systém odměn**: Achievementy a bodování za dokončené lekce
- **SQLite databáze**: Portabilní databáze pro offline i online verzi
- **Responzivní design**: Vhodný pro tablety i počítače
- **Dětský design**: Barevný a přátelský interface

## 📁 Struktura projektu

```
python-kurz/
├── main.py                 # Hlavní FastAPI aplikace
├── database.py             # Databázové modely a konfigurace
├── auth.py                 # Autentifikace a autorizace
├── schemas.py              # Pydantic modely pro API
├── requirements.txt        # Python závislosti
├── README.md              # Tento soubor
├── python_kurz.db         # SQLite databáze (vytvoří se automaticky)
├── templates/             # HTML šablony (Jinja2)
│   ├── base.html          # Základní šablona
│   ├── index.html         # Hlavní stránka
│   ├── kurz.html          # Stránka kurzu
│   ├── lekce.html         # Stránka lekce
│   ├── playground.html    # Python playground
│   ├── profil.html        # Profil studenta
│   ├── login.html         # Přihlašovací stránka
│   └── register.html      # Registrační stránka
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
   
   **Poznámka**: Při prvním spuštění se automaticky vytvoří SQLite databáze s výchozími daty.

5. **Otevřete prohlížeč**
   - Přejděte na: http://localhost:8000
   - Nebo: http://127.0.0.1:8000

## 🗄️ Databáze

Aplikace používá **SQLite databázi** pro maximální portabilitu:

### Výhody SQLite pro tento projekt:
- ✅ **Portabilita** - jeden soubor, snadno se přenáší
- ✅ **Nulová konfigurace** - funguje out-of-the-box
- ✅ **Offline verze** - žádné síťové závislosti
- ✅ **Jednoduché nasazení** - stačí zkopírovat soubor
- ✅ **Dostatečný výkon** - pro vzdělávací platformu více než dostačující

### Databázové tabulky:
- **users** - Uživatelské účty
- **courses** - Kurzy
- **lessons** - Lekce
- **user_progress** - Pokrok uživatelů
- **achievements** - Systém odměn
- **user_achievements** - Získané odměny

### Migrace databáze:
Databáze se vytvoří automaticky při prvním spuštění. Pokud potřebujete resetovat databázi, smažte soubor `python_kurz.db` a restartujte aplikaci.

## 📚 Použití

### Autentifikace
- **Registrace**: Vytvoření nového účtu
- **Přihlášení**: Bezpečné přihlášení s JWT tokeny
- **Profil**: Správa osobních údajů
- **Odhlášení**: Bezpečné ukončení session

### Hlavní stránka
- Přehled všech dostupných kurzů
- Statistiky pokroku studenta (pouze pro přihlášené)
- Rychlé akce (Playground, Profil)
- Přihlašovací/registrační odkazy

### Kurzy
- **Úvod do Pythonu**: Základní koncepty programování
- **Základy Pythonu**: Proměnné, podmínky, cykly
- **Pokročilé koncepty**: Funkce, seznamy, soubory

### Python Playground
- Interaktivní editor pro testování kódu
- Spouštění Python kódu na serveru
- Předpřipravené příklady
- Zobrazení výstupu a chyb

### Profil studenta (pouze pro přihlášené)
- Sledování dokončených lekcí
- Pokrok v jednotlivých kurzech
- Systém odměn a achievementů
- Celkové skóre a statistiky
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

## 🚀 Nasazení

### Online verze (VPS/Cloud)
1. **Nahrajte soubory** na server
2. **Nainstalujte závislosti**: `pip install -r requirements.txt`
3. **Spusťte aplikaci**: `python main.py`
4. **Nastavte reverse proxy** (nginx/apache) pro port 8000
5. **Databáze se vytvoří automaticky**

### Offline verze (PC)
1. **Stáhněte celý projekt** včetně `python_kurz.db`
2. **Nainstalujte Python** a závislosti
3. **Spusťte**: `python main.py`
4. **Otevřete**: http://localhost:8000

### Portabilní verze
- **SQLite databáze** je jeden soubor - snadno se přenáší
- **Žádné externí závislosti** - funguje offline
- **Jednoduché zálohování** - stačí zkopírovat celou složku

## 📞 Podpora

Pro technickou podporu nebo dotazy:
- Zkontrolujte tento README
- Prohlédněte si kód v `main.py`
- Zkuste restartovat aplikaci

## 📄 Licence

Tento projekt je vytvořen pro vzdělávací účely. Můžete ho volně používat a upravovat.

---

**Vytvořeno s ❤️ pro výuku Pythonu na základních školách**
