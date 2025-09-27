# 🚀 Nasazení na Vercel

## 📋 Předpoklady
- GitHub účet
- Vercel účet (zdarma na vercel.com)
- Přístup k GitHub repozitáři

## 🔧 Kroky nasazení

### 1. **Připravte repozitář**
```bash
# Commitněte všechny změny
git add .
git commit -m "Připraveno pro Vercel deployment"
git push origin main
```

### 2. **Přihlaste se na Vercel**
1. Jděte na https://vercel.com
2. Přihlaste se pomocí GitHub účtu
3. Klikněte na "New Project"

### 3. **Importujte projekt**
1. Vyberte GitHub repozitář
2. Vercel automaticky detekuje FastAPI
3. Nastavte:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (nebo nechte prázdné)
   - **Build Command**: (nechte prázdné)
   - **Output Directory**: (nechte prázdné)

### 4. **Environment Variables** (volitelné)
V Settings → Environment Variables přidejte:
- `SECRET_KEY`: náhodný řetězec pro JWT tokeny

### 5. **Deploy**
1. Klikněte na "Deploy"
2. Počkejte na dokončení (2-3 minuty)
3. Získáte URL: `https://your-project.vercel.app`

## ⚠️ **Důležité poznámky**

### **SQLite na Vercel:**
- ✅ **Funguje** pro testování a malé projekty
- ❌ **Není persistentní** - data se ztratí při redeploy
- 🔄 **Resetuje se** při každém restartu

### **Alternativy pro produkci:**
1. **Vercel Postgres** (doporučeno)
2. **PlanetScale** (MySQL)
3. **Supabase** (PostgreSQL)
4. **Railway** (PostgreSQL)

## 🔄 **Migrace na persistentní databázi**

Pokud chcete zachovat data, doporučuji:

### **Vercel Postgres:**
```bash
# V Vercel dashboard
1. Jděte do projektu
2. Storage → Create Database
3. Vyberte Postgres
4. Zkopírujte connection string
5. Aktualizujte database.py
```

### **Aktualizace kódu:**
```python
# Místo SQLite
DATABASE_URL = "sqlite:///./python_kurz.db"

# Použijte Postgres
DATABASE_URL = "postgresql://user:pass@host:port/db"
```

## 📊 **Monitoring**

V Vercel dashboard můžete sledovat:
- **Functions**: výkon API endpointů
- **Analytics**: návštěvnost
- **Logs**: chyby a debug info

## 🎯 **Výsledek**

Po nasazení budete mít:
- ✅ **Online verzi** na vlastní doméně
- ✅ **Automatické HTTPS**
- ✅ **CDN** pro rychlé načítání
- ✅ **Automatické deploymenty** při push do GitHub

## 🔧 **Lokální testování**

```bash
# Nainstalujte Vercel CLI
npm i -g vercel

# Spusťte lokálně
vercel dev
```

## 📞 **Podpora**

Pokud narazíte na problémy:
1. Zkontrolujte Vercel logs
2. Ověřte environment variables
3. Zkontrolujte GitHub permissions