# 🔧 Oprava registrace - Directus setup

## **🔍 Problémy identifikovány:**

### **1. Chybí kolekce `users`**
- Aplikace se snaží vytvořit uživatele v neexistující kolekci `users`
- Directus má vestavěný systém `directus_users`, ale naše aplikace potřebuje vlastní `users`

### **2. Chybí oprávnění pro Public roli**
- Public role nemá nastavená oprávnění pro čtení dat
- API vrací 403 Forbidden

### **3. Directus auth vs. naše aplikace**
- Directus používá vlastní autentifikaci
- Naše aplikace potřebuje vlastní users kolekci

## **🚀 Řešení:**

### **Krok 1: Vytvoření users kolekce**

1. **Otevřete Directus admin**: http://188.245.190.72:8057/admin
2. **Přejděte na**: Settings > Data Model
3. **Klikněte**: "Create Collection"
4. **Nastavte**:
   - **Collection Name**: `users`
   - **Display Name**: `Uživatelé`
   - **Icon**: `people_alt`
   - **Note**: `Uživatelé aplikace`
5. **Klikněte**: "Create Collection"

### **Krok 2: Přidání polí do users kolekce**

**Přidejte tato pole:**

#### **A) ID (automatické)**
- **Field**: `id`
- **Type**: Integer
- **Primary Key**: ✅
- **Auto Increment**: ✅

#### **B) Uživatelské jméno**
- **Field**: `username`
- **Type**: String
- **Required**: ✅
- **Unique**: ✅
- **Max Length**: 100

#### **C) Email**
- **Field**: `email`
- **Type**: String
- **Required**: ✅
- **Unique**: ✅
- **Max Length**: 200

#### **D) Heslo**
- **Field**: `password`
- **Type**: String
- **Required**: ✅
- **Hidden**: ✅
- **Max Length**: 255

#### **E) Celé jméno**
- **Field**: `full_name`
- **Type**: String
- **Required**: ❌
- **Max Length**: 200

#### **F) Status**
- **Field**: `status`
- **Type**: String
- **Default**: `active`
- **Choices**: `active`, `inactive`

### **Krok 3: Nastavení oprávnění pro Public roli**

1. **Přejděte na**: Settings > Access Policies
2. **Klikněte**: "Public Policy"
3. **V sekci Permissions**:
   - **Klikněte**: "Add Collection"
   - **Collection**: `courses`
   - **Actions**: `read` ✅
   - **Klikněte**: "Add Collection"
   - **Collection**: `lessons`
   - **Actions**: `read` ✅
   - **Klikněte**: "Add Collection"
   - **Collection**: `users`
   - **Actions**: `create` ✅, `read` ✅
4. **Klikněte**: "Save"

### **Krok 4: Nastavení oprávnění pro Authenticated roli**

1. **Přejděte na**: Settings > Access Policies
2. **Klikněte**: "Authenticated Policy"
3. **V sekci Permissions**:
   - **Přidejte všechny kolekce** s oprávněními:
     - `courses`: `read` ✅
     - `lessons`: `read` ✅
     - `users`: `read` ✅, `update` ✅
     - `user_progress`: `create` ✅, `read` ✅, `update` ✅
     - `achievements`: `read` ✅
     - `user_achievements`: `create` ✅, `read` ✅, `update` ✅
4. **Klikněte**: "Save"

### **Krok 5: Aktualizace aplikace**

**Opravte `data_service.py`:**

```python
async def register_user(self, email: str, password: str, first_name: str, last_name: str) -> Optional[Dict]:
    """Registrace nového uživatele přes Directus"""
    try:
        # Použijte users kolekci místo directus_users
        user_data = {
            "username": email.split("@")[0],  # Použijte email jako username
            "email": email,
            "password": password,
            "full_name": f"{first_name} {last_name}".strip(),
            "status": "active"
        }
        
        result = await self.directus.create_item("users", user_data)
        if result:
            print(f"User registered successfully: {email}")
            return result
        else:
            print(f"Failed to register user: {email}")
            return None
    except Exception as e:
        print(f"Registration error: {e}")
        return None
```

### **Krok 6: Test registrace**

1. **Restartujte aplikaci**: `python main.py`
2. **Otevřete**: http://localhost:8000/register
3. **Vyplňte formulář** a zkuste registraci
4. **Zkontrolujte** v Directus admin, zda se uživatel vytvořil

## **🎯 Výsledek:**

- ✅ **Users kolekce vytvořena**
- ✅ **Oprávnění nastavena**
- ✅ **Registrace funguje**
- ✅ **Aplikace připravena**

---

**💡 Tip**: Pokud stále nefunguje, zkontrolujte Directus logy a oprávnění pro každou kolekci.
