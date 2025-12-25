# Souhrn práce s Directus serverem a instancemi

## 🖥️ Server a prostředí
- **OS**: Windows (win32 10.0.26100)
- **Shell**: PowerShell
- **Projekt**: C:\Users\Dasa\Pythonprojekt

## 🔧 Co jsme dělali s Directus

### 1. Environment Variables a konfigurace
**Soubory:**
- Měli jsme `env.local`, který jsme přejmenovali na `.env`
- V `.env` jsou tyto proměnné:
  - `SECRET_KEY` - pro JWT tokeny
  - `DIRECTUS_URL` - URL Directus instance
  - `DIRECTUS_TOKEN` - API token pro autentizaci
  - `ACCESS_TOKEN_EXPIRE_MINUTES=30` - expirační čas tokenů

**Pro Vercel:**
- Všechny tyto proměnné jsme přidali do Vercel Environment Variables
- Po přidání byl proveden redeploy

### 2. Directus instance pro Python učební platformu (appdílna)

#### Problémy, které jsme řešili:

**A) Registrace studenta nefungovala**
- **Problém**: Directus vracel status 204 (No Content) při úspěšné registraci, ale aplikace to brala jako failure
- **Řešení**: 
  - Upravili jsme `directus_client.py` aby správně rozpoznal status 204 jako success
  - Přidali jsme debug logging do všech souborů:
    - `directus_client.py` - logování Directus responses
    - `data_service.py` - trace return values
    - `main.py` - inspect register_result

**B) Directus kolekce `students` chyběla nebo měla špatné Access Policy**
- **Checklist pro správnou konfiguraci Directus:**
  1. Vytvořit kolekci `students` s těmito poli:
     - `id` (UUID, Primary Key)
     - `username` (String, unique)
     - `email` (String, unique)
     - `password` (Hash)
     - `first_name` (String)
     - `last_name` (String)
     - `date_created` (Timestamp)
     - `status` (String, default: "active")
  
  2. Nastavit Public Access Policy:
     - **Create**: Povolit (pro registraci)
     - **Read**: Povolit (pro přihlášení)
     - Ostatní akce podle potřeby

**C) Přihlášení**
- Původně endpoint očekával `email`, změnili jsme na `username`
- TODO: Implementovat správné ověření hesla (teď je to temporary bez password verification)
- JWT token se ukládá do cookie s `SameSite=Lax`

**D) Autentizace flow**
1. User se registruje → vytvoří se záznam v Directus `students`
2. Po registraci dostane JWT token a je přihlášen
3. Token se kontroluje v `auth_directus.py`:
   - První kontrola: cookies (`access_token`)
   - Druhá kontrola: Authorization header
4. `get_current_user_optional` vrací objekt s `username` a `full_name`

### 3. Directus logs a debugging

**Log z PowerShellu ukázal:**
```
POST /items/students 204 1ms
```
- Status 204 = úspěšná operace bez content
- To byl klíč k vyřešení problému s registrací

### 4. Aktuální stav kódu

**Soubory upravené kvůli Directus:**
- `directus_client.py` - handle 204 status, debug logging
- `data_service.py` - debug logging pro register flow
- `main.py` - `/register` endpoint s debuggingem, `/login` endpoint změněn na username
- `auth_directus.py` - cookie-first authentication
- `templates/register.html` - správné nastavení cookie, redirect
- `templates/login.html` - FormData místo JSON

## ❌ Co teď nefunguje

### Problém s Directus instancemi:

**1. Directus pro appdílnu (Python platforma) - NEFUNGUJE**
- Instance pravděpodobně neběží nebo není dostupná

**2. Directus pro dropshipping (eshop) - NEFUNGUJE**
- Instance neodpovídá

### ⚠️ DŮLEŽITÝ KONTEXT - Co jsme dělali před tím:

**Manipulace s Docker a Redis:**
- ✅ Měnili jsme `docker-compose.yml` nebo `docker-compose.config`
- ✅ Pracovali jsme s Redis konfigurací
- ✅ **Pokusili jsme se o hromadný restart Docker kontejnerů**
- ⚠️ **Při restartu jsme možná vypli Directus instance**

**Pravděpodobná příčina:**
- Docker kontejnery s Directus se **zastavily** při hromadném restartu
- Kontejnery se **automaticky nespustily zpět**
- Možný conflict v docker-compose konfiguraci
- Redis restart mohl způsobit problém s závislostmi

**Co to znamená:**
- ✅ **Data v databázi jsou pravděpodobně v pořádku** (uložená v Docker volumes)
- ❌ Docker kontejnery jsou stopped nebo v error stavu
- ❌ Možný port conflict mezi kontejnery
- ❌ Redis dependency problém

### Diagnostika pro Claude.ai:

**Kritické otázky k prověření:**
1. **Jak zjistit stav všech Docker kontejnerů?** (běžící/stopped/error)
2. **Jak identifikovat Directus kontejnery?** (pro appdílnu i dropshipping)
3. **Jak bezpečně restartovat zastavené Directus kontejnery?**
4. **Jak zkontrolovat Docker volumes** (že databázová data jsou stále tam)?
5. **Jak ověřit Redis kontejner a jeho připojení?**
6. **Jak řešit port conflicts mezi kontejnery?**
7. **Kde najít Docker logy pro Directus?** (error messages)
8. **Jak ověřit docker-compose.yml konfiguraci?**
9. **Jak zkontrolovat dependencies mezi kontejnery?** (depends_on)
10. **Jak zkontrolovat/regenerovat API tokeny po restartu?**

**Důležité příkazy pro diagnostiku:**
```powershell
# 1. Zobrazit VŠECHNY kontejnery (běžící i zastavené)
docker ps -a

# 2. Zobrazit Docker volumes (tam jsou data!)
docker volume ls

# 3. Zkontrolovat logy konkrétního kontejneru
docker logs <container_name_or_id>
docker logs <container_name_or_id> --tail 100

# 4. Zkontrolovat docker-compose služby
docker-compose ps

# 5. Zkontrolovat které porty jsou obsazené
netstat -ano | findstr "8055"
netstat -ano | findstr "6379"  # Redis

# 6. Inspektovat kontejner (konfigurace, volumes, network)
docker inspect <container_name_or_id>

# 7. Zkontrolovat Docker networks
docker network ls
docker network inspect <network_name>
```

**Možné postupy pro restart:**
```powershell
# POSTUP A: Restart konkrétního kontejneru
docker start <directus_container_name>

# POSTUP B: Restart všech služeb v docker-compose
cd cesta\k\docker-compose\souboru
docker-compose up -d

# POSTUP C: Kompletní rebuild (pokud je problém s konfigurací)
docker-compose down
docker-compose up -d --build

# POSTUP D: Restart jen Directus služeb (pokud jsou pojmenované)
docker-compose restart directus-appdilna
docker-compose restart directus-dropshipping

# VAROVÁNÍ: NEPOUŽÍVAT pokud nechceš ztratit data:
# docker-compose down -v  # <-- SMAŽE VOLUMES!
```

**Kontrola integrity dat:**
```powershell
# Zkontrolovat že volumes existují
docker volume inspect <volume_name>

# Připojit se k databázi uvnitř kontejneru
docker exec -it <directus_container> sh
# Pak uvnitř:
# psql -U postgres -d directus  (pro PostgreSQL)
# mysql -u root -p directus     (pro MySQL)
```

## 📁 Struktura projektu

**Python Learning Platform:**
```
Pythonprojekt/
├── .env (SECRET_KEY, DIRECTUS_URL, DIRECTUS_TOKEN)
├── main.py (FastAPI app)
├── directus_client.py (Directus API komunikace)
├── data_service.py (abstrakce nad Directus)
├── auth_directus.py (JWT autentizace)
├── templates/ (HTML šablony)
├── static/ (CSS, JS, assets)
└── requirements.txt
```

## 🔑 Klíčové koncepty

1. **Directus jako headless CMS** - ukládá data (students, courses, lessons)
2. **FastAPI backend** - Python web framework
3. **JWT tokeny** - pro session management
4. **Cookie-based auth** - token v HTTP-only cookie
5. **Status 204 handling** - Directus vrací 204 při success bez content

## ⚠️ DŮLEŽITÉ pro debugging

**Když nefunguje Directus:**
1. Zkontrolovat, že instance běží (proces/docker container)
2. Ověřit správnost `DIRECTUS_URL` (včetně portu)
3. Zkontrolovat `DIRECTUS_TOKEN` (možná vypršel)
4. Zkousnout API call ručně (curl/Postman) k Directus endpointu
5. Podívat se do Directus Admin UI (pokud je dostupný)
6. Zkontrolovat logy Directus instance

**Příklad testu API:**
```bash
curl -X GET "http://localhost:8055/items/students" \
  -H "Authorization: Bearer YOUR_DIRECTUS_TOKEN"
```

## 📊 Co funguje (v kódu)

✅ Registrace flow v kódu (když Directus odpovídá)
✅ Login flow v kódu (když Directus odpovídá)
✅ JWT autentizace
✅ Cookie handling
✅ Status 204 recognition
✅ Debug logging

## ❓ Co potřebuješ od Claude.ai

### 🎯 Hlavní cíl:
**Bezpečně restartovat Directus instance pro appdílnu a dropshipping, které se zastavily při Docker restartu, BEZ ZTRÁTY DAT.**

### 📋 Konkrétní kroky k vyřešení:

1. **Jak zjistit stav Docker kontejnerů?**
   - Seznam všech kontejnerů (běžící i zastavené)
   - Identifikace Directus kontejnerů
   - Zjištění proč se zastavily (logy)

2. **Jak zkontrolovat že data jsou v pořádku?**
   - Verifikace Docker volumes
   - Kontrola databázových souborů
   - Backup strategie (pro jistotu)

3. **Jak bezpečně restartovat?**
   - Správné pořadí (Redis → Database → Directus?)
   - Kontrola portů a conflicts
   - Ověření že se vše spustilo správně

4. **Jak opravit docker-compose.yml pokud je problém?**
   - Kontrola depends_on dependencies
   - Ověření restart policies
   - Síťová konfigurace

5. **Post-restart checklist:**
   - Test API endpointů
   - Regenerace tokenů pokud potřeba
   - Ověření že aplikace se připojuje

### 🚨 KRITICKÁ POZNÁMKA:
**NESMÍME použít `docker-compose down -v` protože by to smazalo volumes s daty!**

### 💡 Ideální odpověď od Claude.ai:
Krok-za-krokem návod jak:
1. Diagnostikovat současný stav
2. Identifikovat problém
3. Bezpečně restartovat
4. Ověřit že vše funguje
5. Prevence do budoucna (auto-restart policies)

---

**Poznámka**: Všechno výše je z práce na Python learning platform. Pro dropshipping eshop bude pravděpodobně podobná situace, ale s jiným Directus instance URL a tokenem.

