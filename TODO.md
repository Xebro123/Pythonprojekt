# TODO - Python Learning Platform

## ✅ Hotovo
- [x] Registrace a přihlášení studentů
- [x] JWT autentizace s cookies
- [x] Základní dashboard s přehledem kurzů
- [x] Playground pro Python a JavaScript
- [x] Metalické modré buttony s 3D efektem
- [x] ÚKOL 1: Předlekce s cool želvou Terry
  - Animovaná želva na skateboardu se slunečními brýlemi a čepicí
  - Typewriter efekt s barevnými bublonami textu
  - Skip a Pause/Resume tlačítka
  - Layout: želva vlevo (menší), text vpravo
- [x] Python Dashboard (`/python`) se seznamem lekcí
- [x] Navigační tlačítka v lekcích (Pokračovat, Zpět na seznam lekcí)
- [x] Responzivní design Python Dashboardu pro mobily

## 📝 Rozpracováno

### ÚKOL 2: Lekce 1 - Live Python editor s turtle graphics
**Popis ze zadání:**
- Interaktivní Python editor přímo v prohlížeči
- Turtle graphics výstup vedle editoru
- Studenti mohou psát kód a vidět výsledek v reálném čase
- Úkoly: nakreslit čtverec, trojúhelník, kruh
- Testování kódu s automatickým vyhodnocením
- Nápovědy a tipy při chybách

**Technické požadavky:**
- Backend: Spustit Python s turtle modulem na serveru
- Frontend: Monaco Editor nebo CodeMirror pro editor
- Canvas nebo SVG pro zobrazení turtle výstupu
- WebSocket pro real-time komunikaci?
- Sandbox prostředí pro bezpečné spouštění kódu

## 🔜 Čeká na implementaci

### ÚKOL 3: Lekce 2 - Smyčky a opakování
**Ze zadání:**
- Vysvětlení `for` a `while` smyček
- Praktické cvičení s opakováním kreslení
- Úkoly: nakreslit mřížku, spirálu, květinu
- Interaktivní příklady
- Mini-kvízy na pochopení konceptu

### ÚKOL 4: Lekce 3 - Práce s barvami
**Ze zadání:**
- RGB hodnoty a barvy
- Náhodné barvy
- Gradientové efekty
- Úkoly: vytvořit duhový vzor, barevnou spirálu
- Kreativní projekty

### ÚKOL 5: Další lekce Python kurzu
- Lekce 4: Funkce a parametry
- Lekce 5: Podmínky (if/elif/else)
- Lekce 6: Seznamy a manipulace s daty
- Lekce 7: Slovníky a struktury
- Lekce 8: Závěrečný projekt

### ÚKOL 6: AI Kurz
- Úvodní lekce o AI
- Základy strojového učení
- Práce s daty
- Trénování modelů
- Interaktivní ukázky

### ÚKOL 7: JavaScript Kurz
- Podobná struktura jako Python kurz
- Úvodní lekce s cool postavičkou
- Interaktivní editor
- DOM manipulace
- Animace a hry

## 🔧 Technické úkoly

### Autentizace a bezpečnost
- [ ] TODO v `main.py`: Implementovat správné ověření hesla při přihlášení
- [ ] Možnost přihlášení pomocí email NEBO username
- [ ] Resetování hesla
- [ ] Email verifikace

### Directus integrace
- [ ] Propojení s Directus kolekcemi pro lekce
- [ ] Ukládání pokroku studenta
- [ ] Tracking dokončených úkolů
- [ ] Bodový systém / odznaky

### UI/UX vylepšení
- [ ] Responzivní design pro všechny stránky (ne jen Python Dashboard)
- [ ] Loading stavy při načítání dat
- [ ] Error handling a uživatelské zprávy
- [ ] Animace přechodů mezi stránkami
- [ ] Dark mode?

### Deployment
- [ ] Vercel Environment Variables správně nastaveny
- [ ] Production build optimalizace
- [ ] CDN pro statické soubory
- [ ] Monitoring a error tracking

## 📊 Progress tracking
- [ ] Databázové schéma pro student progress
- [ ] API endpointy pro ukládání/načítání pokroku
- [ ] Vizualizace pokroku na dashboardu
- [ ] Certifikáty po dokončení kurzu

## 🎨 Design System
- [ ] Konzistentní barevná paleta napříč aplikací
- [ ] Komponenty pro opakující se UI prvky
- [ ] Typography guidelines
- [ ] Ikony a ilustrace

## 🧪 Testing
- [ ] Unit testy pro backend
- [ ] Integration testy
- [ ] E2E testy pro kritické flow
- [ ] Testování na různých zařízeních

## 📝 Poznámky
- Všechny environment variables (`SECRET_KEY`, `DIRECTUS_URL`, `DIRECTUS_TOKEN`, `ACCESS_TOKEN_EXPIRE_MINUTES`) musí být v Vercel Environment Variables
- Directus kolekce `students` musí mít správné Access Policy (Public Create/Read)
- Playground aktuálně podporuje Python (server-side) a JavaScript (client-side)

