# 🚀 Rychlý Setup Directus

## **Automatické nastavení za 5 minut!**

### **1. Spuštění automatického setup:**
```bash
python run_setup.py
```

### **2. Zadejte admin údaje:**
- **Email**: `admin@example.com` (nebo váš admin email)
- **Heslo**: `admin123` (nebo vaše admin heslo)

### **3. Script automaticky:**
- ✅ Přihlásí se do Directus
- ✅ Vytvoří všechny kolekce (courses, lessons, user_progress, achievements, user_achievements)
- ✅ Nastaví všechna pole a vztahy
- ✅ Vytvoří ukázková data (3 kurzy, 10 lekcí, 4 achievementy)

### **4. Vytvoření Directus token:**
1. Přejděte na: `http://188.245.190.72:8057/admin/settings/access-tokens`
2. Klikněte "Create Token"
3. Zadejte název: "Python Kurz API"
4. Vyberte oprávnění: "Full Access"
5. Zkopírujte token

### **5. Nastavení .env souboru:**
```bash
# Zkopírujte env.local do .env
cp env.local .env

# Upravte DIRECTUS_TOKEN v .env souboru
DIRECTUS_TOKEN=your-copied-token-here
```

### **6. Spuštění aplikace:**
```bash
# Nainstalujte závislosti
pip install -r requirements.txt

# Spusťte aplikaci
python main.py
```

### **7. Otevřete v prohlížeči:**
- **Lokální**: http://localhost:8000
- **Vercel**: https://your-app.vercel.app

## **🎯 Co script vytvoří:**

### **Kolekce:**
- **courses** - Kurzy programování
- **lessons** - Lekce kurzů  
- **user_progress** - Pokrok uživatelů
- **achievements** - Odměny a úspěchy
- **user_achievements** - Získané odměny

### **Ukázková data:**
- **3 kurzy**: Úvod, Základy, Pokročilé
- **10 lekcí**: Kompletní obsah s příklady kódu
- **4 achievementy**: Odměny za pokrok

### **Automatické nastavení:**
- ✅ Všechna pole a datové typy
- ✅ Vztahy mezi kolekcemi
- ✅ Oprávnění a přístup
- ✅ Ukázkový obsah

## **🔧 Ruční setup (pokud automatický nefunguje):**

### **1. Přihlášení do Directus:**
- URL: `http://188.245.190.72:8057/admin`
- Email: váš admin email
- Heslo: vaše admin heslo

### **2. Vytvoření kolekcí:**
- Přejděte na Settings > Data Model
- Klikněte "Create Collection"
- Vytvořte všechny kolekce podle `DIRECTUS_SETUP.md`

### **3. Nastavení oprávnění:**
- Settings > Roles & Permissions
- Public role: čtení kurzů a lekcí
- Authenticated role: všechny operace

## **🐛 Troubleshooting:**

### **Chyba přihlášení:**
- Zkontrolujte admin email a heslo
- Ověřte, že máte admin oprávnění

### **Chyba vytváření kolekcí:**
- Zkontrolujte, že máte oprávnění k vytváření kolekcí
- Restartujte Directus server

### **Chyba API:**
- Zkontrolujte DIRECTUS_URL v .env
- Ověřte, že token má správná oprávnění

## **📞 Podpora:**
- Zkontrolujte Directus logy
- Ověřte PostgreSQL připojení
- Testujte API endpointy přímo

---

**🎉 Po dokončení setup máte plně funkční online verzi s Directus + PostgreSQL!**
