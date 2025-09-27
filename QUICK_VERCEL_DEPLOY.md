# 🚀 Rychlé nasazení na Vercel

## ⚡ **5 minut k nasazení!**

### **1. Commitněte změny**
```bash
git add .
git commit -m "Základní verze s autentifikací a databází"
git push origin main
```

### **2. Nasaďte na Vercel**
1. Jděte na https://vercel.com
2. Přihlaste se s GitHub účtem
3. Klikněte "New Project"
4. Vyberte váš repozitář
5. Klikněte "Deploy"

### **3. Nastavte Environment Variables** (volitelně)
V Settings → Environment Variables:
- `SECRET_KEY`: náhodný řetězec (např. `my-super-secret-key-123`)

### **4. Hotovo!** 🎉
- Aplikace běží na `https://your-project.vercel.app`
- SQLite databáze se vytvoří automaticky
- Můžete se registrovat a testovat

## ⚠️ **Důležité upozornění**

**SQLite na Vercel:**
- ✅ Funguje pro testování
- ❌ Data se ztratí při redeploy
- 🔄 Vhodné jen pro vývoj

## 🔄 **Později migrujte na VPS**

Když budete mít Directus připravený:
1. Exportujte data z Vercel
2. Importujte do PostgreSQL na VPS
3. Přepněte doménu na VPS

## 📱 **Co můžete testovat hned:**

- ✅ Registrace nového účtu
- ✅ Přihlášení/odhlášení
- ✅ Procházení kurzů
- ✅ Python Playground
- ✅ Profil (základní)
- ✅ Sledování pokroku

## 🎯 **Pro syna:**

- Může se zaregistrovat
- Vidí svůj pokrok
- Může testovat funkce
- Má radost z pokroků! 😊