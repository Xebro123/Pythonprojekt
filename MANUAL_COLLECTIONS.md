# 📚 Manuální vytvoření kolekcí v Directus

## **Problém s automatickým scriptem:**
Script se spouští, ale kolekce se nevytvářejí. Pojďme to vyřešit manuálně.

## **🚀 Postup:**

### **1. Otevřete Directus admin panel:**
```
http://188.245.190.72:8057/admin
```

### **2. Přihlaste se:**
- **Email**: `admin@ngc.com`
- **Heslo**: `ngc_admin_789`

### **3. Vytvořte kolekce (Settings > Data Model):**

#### **A) Kurzy (courses):**
1. Klikněte **"Create Collection"**
2. **Collection Name**: `courses`
3. **Display Name**: `Kurzy`
4. **Icon**: `school`
5. **Note**: `Kurzy programování`
6. Klikněte **"Create Collection"**

**Přidejte pole:**
- `id` (Integer, Primary Key, Auto Increment)
- `title` (String, Required) - Název kurzu
- `description` (Text) - Popis kurzu
- `level` (String) - Úroveň (uvod/zaklady/pokrocile)
- `status` (String) - Status (published/draft)
- `sort` (Integer) - Pořadí

#### **B) Lekce (lessons):**
1. Klikněte **"Create Collection"**
2. **Collection Name**: `lessons`
3. **Display Name**: `Lekce`
4. **Icon**: `book`
5. **Note**: `Lekce kurzů`
6. Klikněte **"Create Collection"**

**Přidejte pole:**
- `id` (Integer, Primary Key, Auto Increment)
- `course` (Integer, Foreign Key → courses) - Kurz
- `lesson_number` (Integer, Required) - Číslo lekce
- `title` (String, Required) - Název lekce
- `description` (Text) - Popis lekce
- `content` (Text) - Obsah lekce
- `code_example` (Text) - Příklad kódu
- `status` (String) - Status (published/draft)
- `sort` (Integer) - Pořadí

#### **C) Pokrok uživatelů (user_progress):**
1. Klikněte **"Create Collection"**
2. **Collection Name**: `user_progress`
3. **Display Name**: `Pokrok uživatelů`
4. **Icon**: `trending_up`
5. **Note**: `Pokrok uživatelů v lekcích`
6. Klikněte **"Create Collection"**

**Přidejte pole:**
- `id` (Integer, Primary Key, Auto Increment)
- `user` (UUID, Foreign Key → directus_users) - Uživatel
- `lesson` (Integer, Foreign Key → lessons) - Lekce
- `completed` (Boolean) - Dokončeno
- `completion_percentage` (Float) - Procento dokončení
- `time_spent` (Integer) - Čas strávený (sekundy)
- `completed_at` (DateTime) - Dokončeno dne

#### **D) Achievementy (achievements):**
1. Klikněte **"Create Collection"**
2. **Collection Name**: `achievements`
3. **Display Name**: `Odměny`
4. **Icon**: `emoji_events`
5. **Note**: `Odměny a úspěchy`
6. Klikněte **"Create Collection"**

**Přidejte pole:**
- `id` (Integer, Primary Key, Auto Increment)
- `name` (String, Required) - Název
- `description` (Text) - Popis
- `icon` (String) - Ikona (FontAwesome)
- `points` (Integer) - Body
- `condition_type` (String) - Typ podmínky
- `condition_value` (Integer) - Hodnota podmínky
- `status` (String) - Status (published/draft)

#### **E) Uživatelské achievementy (user_achievements):**
1. Klikněte **"Create Collection"**
2. **Collection Name**: `user_achievements`
3. **Display Name**: `Uživatelské odměny`
4. **Icon**: `star`
5. **Note**: `Získané odměny uživatelů`
6. Klikněte **"Create Collection"**

**Přidejte pole:**
- `id` (Integer, Primary Key, Auto Increment)
- `user` (UUID, Foreign Key → directus_users) - Uživatel
- `achievement` (Integer, Foreign Key → achievements) - Achievement
- `earned_at` (DateTime) - Získáno dne

### **4. Nastavte oprávnění:**
1. Přejděte na **Settings > Roles & Permissions**
2. **Public role**: čtení kurzů a lekcí
3. **Authenticated role**: všechny operace

### **5. Vytvořte API token:**
1. Přejděte na **Settings > Access Tokens**
2. Klikněte **"Create Token"**
3. **Název**: `Python Kurz API`
4. **Oprávnění**: `Full Access`
5. **Zkopírujte token**

### **6. Aktualizujte .env:**
```bash
# Nahraďte token v .env souboru
DIRECTUS_TOKEN=your-copied-token-here
```

### **7. Spusťte aplikaci:**
```bash
python main.py
```

## **🎯 Výsledek:**
- ✅ Všechny kolekce vytvořeny
- ✅ Pole a vztahy nastaveny
- ✅ Oprávnění konfigurována
- ✅ API token připraven
- ✅ Aplikace funkční

---

**💡 Tip**: Pokud chcete rychlejší postup, můžete použít Directus import/export funkcionalitu pro hromadné vytvoření dat.
