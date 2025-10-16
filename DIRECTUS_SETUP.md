# Directus Setup pro Online Verzi

## 📋 Požadavky

### 1. Directus Server
- ✅ **URL**: `http://188.245.190.72:8057`
- ✅ **PostgreSQL databáze** připojená
- ✅ **Admin přístup** k Directus

### 2. Environment Variables
```bash
DIRECTUS_URL=http://188.245.190.72:8057
DIRECTUS_TOKEN=your-directus-token-here
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🗄️ Directus Kolekce

### **Kurzy (courses)**
```json
{
  "id": "integer",
  "course_id": "string (unique)",
  "title": "string",
  "description": "text",
  "level": "string",
  "status": "string (published/draft)",
  "sort": "integer",
  "lessons": "relation (many-to-many)"
}
```

### **Lekce (lessons)**
```json
{
  "id": "integer",
  "course": "relation (many-to-one)",
  "lesson_number": "integer",
  "title": "string",
  "description": "text",
  "content": "text (HTML)",
  "code_example": "text",
  "status": "string (published/draft)",
  "sort": "integer"
}
```

### **Uživatelé (users)**
```json
{
  "id": "integer",
  "email": "string (unique)",
  "password": "string (hashed)",
  "first_name": "string",
  "last_name": "string",
  "status": "string (active/inactive)",
  "date_created": "datetime"
}
```

### **Pokrok uživatelů (user_progress)**
```json
{
  "id": "integer",
  "user": "relation (many-to-one)",
  "lesson": "relation (many-to-one)",
  "completed": "boolean",
  "completion_percentage": "float",
  "time_spent": "integer (seconds)",
  "completed_at": "datetime",
  "date_created": "datetime"
}
```

### **Achievementy (achievements)**
```json
{
  "id": "integer",
  "name": "string (unique)",
  "description": "text",
  "icon": "string (FontAwesome)",
  "points": "integer",
  "condition_type": "string",
  "condition_value": "integer",
  "status": "string (published/draft)"
}
```

### **Uživatelské achievementy (user_achievements)**
```json
{
  "id": "integer",
  "user": "relation (many-to-one)",
  "achievement": "relation (many-to-one)",
  "earned_at": "datetime"
}
```

## 🔧 Setup Kroky

### 1. **Vytvoření kolekcí v Directus**
1. Přejděte na `http://188.245.190.72:8057/admin/settings/data-model`
2. Vytvořte všechny výše uvedené kolekce
3. Nastavte správné vztahy (relations)

### 2. **Nastavení oprávnění**
- **Public role**: Čtení kurzů a lekcí
- **Authenticated role**: Všechny operace s pokrokem
- **Admin role**: Správa všech dat

### 3. **Vytvoření Directus Token**
1. Přejděte na `http://188.245.190.72:8057/admin/settings/access-tokens`
2. Vytvořte nový token s oprávněními pro API
3. Zkopírujte token do `.env` souboru

### 4. **Import výchozích dat**
```python
# Script pro import kurzů a lekcí
python import_data.py
```

## 🚀 Deployment

### **Vercel Deployment**
1. **Environment Variables** v Vercel:
   ```
   DIRECTUS_URL=http://188.245.190.72:8057
   DIRECTUS_TOKEN=your-token
   SECRET_KEY=your-secret
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```

### **VPS Deployment**
1. **Nastavení .env**:
   ```bash
   cp env.example .env
   # Upravte hodnoty v .env
   ```

2. **Spuštění**:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

## 🔍 Testování

### **API Testy**
```bash
# Test Directus připojení
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://188.245.190.72:8057/items/courses

# Test autentifikace
curl -X POST http://localhost:8000/login \
     -d "email=test@example.com&password=password"
```

### **Funkční testy**
1. ✅ **Registrace** nového uživatele
2. ✅ **Přihlášení** existujícího uživatele
3. ✅ **Načtení kurzů** z Directus
4. ✅ **Uložení pokroku** do Directus
5. ✅ **Python Playground** funguje

## 🐛 Troubleshooting

### **Časté problémy**

1. **Directus API chyby**:
   - Zkontrolujte `DIRECTUS_URL` a `DIRECTUS_TOKEN`
   - Ověřte oprávnění tokenu

2. **Autentifikace nefunguje**:
   - Zkontrolujte Directus users kolekci
   - Ověřte hashování hesel

3. **Kurzy se nenačítají**:
   - Zkontrolujte status kolekcí (published)
   - Ověřte vztahy mezi kolekcemi

## 📞 Podpora

Pro technické problémy:
- Zkontrolujte Directus logy
- Ověřte PostgreSQL připojení
- Testujte API endpointy přímo
