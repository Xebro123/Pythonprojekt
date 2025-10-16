# 🚀 Rychlý Manuální Setup Directus

## **Problém s automatickým přihlášením:**
Directus server vrací HTML místo JSON, takže automatický script nefunguje.

## **✅ Řešení - Manuální setup (5 minut):**

### **1. 🌐 Otevřete Directus admin panel:**
```
http://188.245.190.72:8057/admin
```

### **2. 🔐 Přihlaste se:**
- **Email**: `admin@ngc.com`
- **Heslo**: `ngc_admin_789`

### **3. 📚 Vytvořte kolekce (Settings > Data Model):**

#### **A) Kurzy (courses):**
- **Název**: `courses`
- **Pole**:
  - `id` (Integer, Primary Key, Auto Increment)
  - `course_id` (String, Unique, Required)
  - `title` (String, Required)
  - `description` (Text)
  - `level` (String, Choices: uvod/zaklady/pokrocile)
  - `status` (String, Choices: published/draft)
  - `sort` (Integer, Default: 0)

#### **B) Lekce (lessons):**
- **Název**: `lessons`
- **Pole**:
  - `id` (Integer, Primary Key, Auto Increment)
  - `course` (Integer, Foreign Key → courses)
  - `lesson_number` (Integer, Required)
  - `title` (String, Required)
  - `description` (Text)
  - `content` (Text, Rich Text)
  - `code_example` (Text, Code Editor, Language: python)
  - `status` (String, Choices: published/draft)
  - `sort` (Integer, Default: 0)

#### **C) Pokrok uživatelů (user_progress):**
- **Název**: `user_progress`
- **Pole**:
  - `id` (Integer, Primary Key, Auto Increment)
  - `user` (UUID, Foreign Key → directus_users)
  - `lesson` (Integer, Foreign Key → lessons)
  - `completed` (Boolean, Default: false)
  - `completion_percentage` (Float, Default: 0.0)
  - `time_spent` (Integer, Default: 0)
  - `completed_at` (DateTime)

#### **D) Achievementy (achievements):**
- **Název**: `achievements`
- **Pole**:
  - `id` (Integer, Primary Key, Auto Increment)
  - `name` (String, Unique, Required)
  - `description` (Text)
  - `icon` (String, FontAwesome icon)
  - `points` (Integer, Default: 0)
  - `condition_type` (String, Choices: lessons_completed/time_spent/perfect_score)
  - `condition_value` (Integer)
  - `status` (String, Choices: published/draft)

#### **E) Uživatelské achievementy (user_achievements):**
- **Název**: `user_achievements`
- **Pole**:
  - `id` (Integer, Primary Key, Auto Increment)
  - `user` (UUID, Foreign Key → directus_users)
  - `achievement` (Integer, Foreign Key → achievements)
  - `earned_at` (DateTime, Default: CURRENT_TIMESTAMP)

### **4. 🔑 Vytvořte API token:**
- Přejděte na **Settings > Access Tokens**
- Klikněte **"Create Token"**
- **Název**: `Python Kurz API`
- **Oprávnění**: `Full Access`
- **Zkopírujte token**

### **5. 📝 Aktualizujte .env soubor:**
```bash
# Zkopírujte env.local do .env
cp env.local .env

# Upravte DIRECTUS_TOKEN v .env souboru
DIRECTUS_TOKEN=your-copied-token-here
```

### **6. 📊 Přidejte ukázková data:**

#### **Kurzy:**
```json
[
  {
    "course_id": "uvod",
    "title": "Úvod do Pythonu",
    "description": "Seznamte se se základy programování v Pythonu",
    "level": "uvod",
    "status": "published",
    "sort": 1
  },
  {
    "course_id": "zaklady", 
    "title": "Základy Pythonu",
    "description": "Naučte se základní koncepty programování",
    "level": "zaklady",
    "status": "published",
    "sort": 2
  },
  {
    "course_id": "pokrocile",
    "title": "Pokročilé koncepty", 
    "description": "Složitější témata pro pokročilé studenty",
    "level": "pokrocile",
    "status": "published",
    "sort": 3
  }
]
```

#### **Lekce (pro kurz "uvod"):**
```json
[
  {
    "course": 1,
    "lesson_number": 1,
    "title": "Co je Python?",
    "description": "Úvod do programování",
    "content": "<h1>Co je Python?</h1><p>Python je programovací jazyk...</p>",
    "status": "published",
    "sort": 1
  },
  {
    "course": 1,
    "lesson_number": 2, 
    "title": "Instalace Pythonu",
    "description": "Jak nainstalovat Python",
    "content": "<h1>Instalace Pythonu</h1><p>Stáhněte Python z python.org...</p>",
    "status": "published",
    "sort": 2
  },
  {
    "course": 1,
    "lesson_number": 3,
    "title": "První program",
    "description": "Hello World!",
    "content": "<h1>První program</h1><p>Napište print('Hello World!')</p>",
    "code_example": "print('Hello World!')",
    "status": "published",
    "sort": 3
  }
]
```

#### **Achievementy:**
```json
[
  {
    "name": "První kroky",
    "description": "Dokončil jste první lekci",
    "icon": "fas fa-play",
    "points": 10,
    "condition_type": "lessons_completed",
    "condition_value": 1,
    "status": "published"
  },
  {
    "name": "Programátor",
    "description": "Spustil jste kód v Playground",
    "icon": "fas fa-code", 
    "points": 20,
    "condition_type": "lessons_completed",
    "condition_value": 3,
    "status": "published"
  },
  {
    "name": "Výdrž",
    "description": "Učte se 7 dní v řadě",
    "icon": "fas fa-fire",
    "points": 50,
    "condition_type": "time_spent",
    "condition_value": 7,
    "status": "published"
  },
  {
    "name": "Absolvent",
    "description": "Dokončete všechny kurzy",
    "icon": "fas fa-graduation-cap",
    "points": 100,
    "condition_type": "lessons_completed", 
    "condition_value": 10,
    "status": "published"
  }
]
```

### **7. 🚀 Spusťte aplikaci:**
```bash
# Nainstalujte závislosti
pip install -r requirements.txt

# Spusťte aplikaci
python main.py
```

### **8. 🌐 Otevřete v prohlížeči:**
- **Lokální**: http://localhost:8000
- **Vercel**: https://your-app.vercel.app

## **🎯 Výsledek:**
- ✅ Všechny kolekce vytvořeny
- ✅ Ukázková data přidána
- ✅ API token nastaven
- ✅ Aplikace připravena k použití

---

**💡 Tip**: Pokud chcete rychlejší postup, můžete použít Directus import/export funkcionalitu pro hromadné vytvoření dat.
