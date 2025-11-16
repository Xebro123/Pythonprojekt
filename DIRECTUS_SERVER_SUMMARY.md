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
- Možné příčiny:
  - Directus proces není spuštěný
  - Špatná URL v `DIRECTUS_URL`
  - Token vypršel nebo je neplatný
  - Firewall/port blokuje přístup

**2. Directus pro dropshipping (eshop) - NEFUNGUJE**
- Stejný problém
- Instance neodpovídá

### Diagnostika pro Claude.ai:

**Otázky k prověření:**
1. Jak spustit/restartovat Directus instance?
2. Jak zkontrolovat, že Directus běží? (proces, port)
3. Kde jsou Directus instance uloženy na serveru?
4. Jaké jsou správné URL pro jednotlivé instance?
5. Jak zkontrolovat/regenerovat API tokeny?
6. Jsou instance správně nakonfigurovány v databázi?
7. Logují instance chyby někam? Kde najít error logy?

**Možné příkazy k ověření:**
```powershell
# Kontrola běžících Directus procesů
Get-Process | Where-Object {$_.ProcessName -like "*directus*"}

# Kontrola portů (standardně 8055)
netstat -ano | findstr "8055"

# Restart Directus (závisí na instalaci)
# npm run start nebo docker-compose up nebo systemctl restart directus
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

1. **Jak diagnostikovat a restartovat Directus instance?**
2. **Jak ověřit, že instance běží správně?**
3. **Kde najít error logy?**
4. **Jak zkontrolovat database connection?**
5. **Správná konfigurace pro multiple Directus instances na jednom serveru?**
6. **Troubleshooting guide pro nefunkční Directus**

---

**Poznámka**: Všechno výše je z práce na Python learning platform. Pro dropshipping eshop bude pravděpodobně podobná situace, ale s jiným Directus instance URL a tokenem.

