# 🚀 Nasazení na VPS s Directus + PostgreSQL

## 📋 Předpoklady
- VPS s Docker a Docker Compose
- Doména (volitelně)
- SSH přístup k VPS

## 🏗️ Architektura

```
VPS
├── Directus (CMS + API)
├── PostgreSQL (databáze)
├── Python Kurz (FastAPI)
└── Nginx (reverse proxy)
```

## 🔧 Kroky nasazení

### 1. **Připravte VPS**

```bash
# Připojte se na VPS
ssh user@your-vps-ip

# Vytvořte složku pro projekt
mkdir python-kurz
cd python-kurz
```

### 2. **Nastavte Directus + PostgreSQL**

Vytvořte `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: python_kurz
      POSTGRES_USER: python_user
      POSTGRES_PASSWORD: your_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  directus:
    image: directus/directus:latest
    environment:
      KEY: your-secret-key
      SECRET: your-secret-secret
      DB_CLIENT: pg
      DB_HOST: postgres
      DB_PORT: 5432
      DB_DATABASE: python_kurz
      DB_USER: python_user
      DB_PASSWORD: your_secure_password
      ADMIN_EMAIL: admin@yourdomain.com
      ADMIN_PASSWORD: admin_password
    ports:
      - "8055:8055"
    depends_on:
      - postgres

volumes:
  postgres_data:
```

### 3. **Spusťte Directus**

```bash
# Spusťte kontejnery
docker-compose up -d

# Zkontrolujte stav
docker-compose ps
```

### 4. **Nastavte Directus**

1. Otevřete http://your-vps-ip:8055
2. Vytvořte admin účet
3. Vytvořte kolekce pro Python kurz:
   - `users` - uživatelé
   - `courses` - kurzy
   - `lessons` - lekce
   - `user_progress` - pokrok
   - `achievements` - odměny

### 5. **Nastavte Python aplikaci**

```bash
# Naklonujte repozitář
git clone https://github.com/your-username/python-kurz.git
cd python-kurz

# Vytvořte virtuální prostředí
python -m venv venv
source venv/bin/activate

# Nainstalujte závislosti
pip install -r requirements.txt
pip install psycopg2-binary  # PostgreSQL driver
```

### 6. **Aktualizujte databázové připojení**

Vytvořte `database_prod.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# PostgreSQL databáze
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://python_user:your_secure_password@localhost:5432/python_kurz"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Zbytek kódu stejný jako v database.py
```

### 7. **Nastavte environment variables**

Vytvořte `.env`:

```env
DATABASE_URL=postgresql://python_user:your_secure_password@localhost:5432/python_kurz
SECRET_KEY=your-jwt-secret-key
```

### 8. **Nastavte Nginx**

Vytvořte `/etc/nginx/sites-available/python-kurz`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # nebo IP adresa

    # Python aplikace
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Directus admin
    location /admin {
        proxy_pass http://localhost:8055;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 9. **Spusťte aplikaci**

```bash
# Aktivujte Nginx
sudo ln -s /etc/nginx/sites-available/python-kurz /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Spusťte Python aplikaci
cd python-kurz
source venv/bin/activate
python main.py
```

### 10. **Nastavte systemd service**

Vytvořte `/etc/systemd/system/python-kurz.service`:

```ini
[Unit]
Description=Python Kurz FastAPI
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/python-kurz
Environment=PATH=/path/to/python-kurz/venv/bin
ExecStart=/path/to/python-kurz/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Aktivujte service
sudo systemctl enable python-kurz
sudo systemctl start python-kurz
sudo systemctl status python-kurz
```

## 🔐 **SSL certifikát (volitelně)**

```bash
# Nainstalujte Certbot
sudo apt install certbot python3-certbot-nginx

# Získejte certifikát
sudo certbot --nginx -d your-domain.com
```

## 📊 **Monitoring**

```bash
# Zkontrolujte logy
sudo journalctl -u python-kurz -f

# Zkontrolujte databázi
docker-compose exec postgres psql -U python_user -d python_kurz

# Zkontrolujte Directus
curl http://localhost:8055/server/ping
```

## 🎯 **Výsledek**

Po nasazení budete mít:
- ✅ **Online verzi** na vaší doméně
- ✅ **Directus admin** na /admin
- ✅ **PostgreSQL databázi** s persistentními daty
- ✅ **Více uživatelů** současně
- ✅ **Centralizovanou správu** přes Directus

## 🔄 **Synchronizace s offline verzí**

Pro synchronizaci dat mezi online a offline verzí můžete:
1. Exportovat data z Directus API
2. Importovat do offline SQLite databáze
3. Nebo vytvořit sync script