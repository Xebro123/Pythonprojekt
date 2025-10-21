#!/usr/bin/env python3
"""
Oprava Directus setup - vytvoření users kolekce a nastavení oprávnění
"""

import httpx
import asyncio

async def fix_directus_setup():
    """Oprava Directus setup"""
    base_url = "http://188.245.190.72:8057"
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print("Oprava Directus setup")
    print("=" * 40)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Přihlášení
            print("1. Přihlášení...")
            response = await client.post(f"{base_url}/auth/login", json={"email": email, "password": password})
            
            if response.status_code != 200:
                print(f"Chyba přihlášení: {response.status_code}")
                return False
            
            data = response.json()
            token = data["data"]["access_token"]
            print(f"Token: {token[:30]}...")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # 1. Vytvoření users kolekce
            print("\n2. Vytváření users kolekce...")
            users_collection = {
                "collection": "users",
                "meta": {
                    "collection": "users",
                    "icon": "people_alt",
                    "note": "Uživatelé aplikace",
                    "display_template": "{{username}}",
                    "hidden": False,
                    "singleton": False
                },
                "schema": {
                    "name": "users"
                }
            }
            
            response = await client.post(f"{base_url}/collections", json=users_collection, headers=headers)
            print(f"Users kolekce: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print("SUCCESS: Users kolekce vytvořena!")
            else:
                print(f"WARNING: Users kolekce - {response.text[:100]}...")
            
            # 2. Přidání polí do users kolekce
            print("\n3. Přidání polí do users kolekce...")
            user_fields = [
                {
                    "field": "id",
                    "type": "integer",
                    "meta": {
                        "hidden": True,
                        "interface": "input",
                        "readonly": True
                    },
                    "schema": {
                        "is_primary_key": True,
                        "has_auto_increment": True
                    }
                },
                {
                    "field": "username",
                    "type": "string",
                    "meta": {
                        "interface": "input",
                        "display": "Uživatelské jméno",
                        "required": True
                    },
                    "schema": {
                        "is_unique": True,
                        "max_length": 100
                    }
                },
                {
                    "field": "email",
                    "type": "string",
                    "meta": {
                        "interface": "input",
                        "display": "Email",
                        "required": True
                    },
                    "schema": {
                        "is_unique": True,
                        "max_length": 200
                    }
                },
                {
                    "field": "password",
                    "type": "string",
                    "meta": {
                        "interface": "input",
                        "display": "Heslo",
                        "required": True,
                        "hidden": True
                    },
                    "schema": {
                        "max_length": 255
                    }
                },
                {
                    "field": "full_name",
                    "type": "string",
                    "meta": {
                        "interface": "input",
                        "display": "Celé jméno"
                    },
                    "schema": {
                        "max_length": 200
                    }
                },
                {
                    "field": "status",
                    "type": "string",
                    "meta": {
                        "interface": "select-dropdown",
                        "display": "Status",
                        "options": {
                            "choices": [
                                {"text": "Aktivní", "value": "active"},
                                {"text": "Neaktivní", "value": "inactive"}
                            ]
                        }
                    },
                    "schema": {
                        "default_value": "active",
                        "max_length": 20
                    }
                }
            ]
            
            for field in user_fields:
                try:
                    response = await client.post(f"{base_url}/fields/users", json=field, headers=headers)
                    print(f"  Pole {field['field']}: {response.status_code}")
                except Exception as e:
                    print(f"  Pole {field['field']}: Exception - {e}")
            
            # 3. Nastavení oprávnění pro Public roli
            print("\n4. Nastavení oprávnění pro Public roli...")
            
            # Získání Public role ID
            response = await client.get(f"{base_url}/roles", headers=headers)
            if response.status_code == 200:
                roles = response.json().get("data", [])
                public_role = None
                for role in roles:
                    if role.get("name") == "Public":
                        public_role = role
                        break
                
                if public_role:
                    print(f"Public role ID: {public_role['id']}")
                    
                    # Nastavení oprávnění pro Public roli
                    permissions = [
                        {
                            "collection": "courses",
                            "action": "read",
                            "role": public_role["id"]
                        },
                        {
                            "collection": "lessons", 
                            "action": "read",
                            "role": public_role["id"]
                        },
                        {
                            "collection": "users",
                            "action": "create",
                            "role": public_role["id"]
                        },
                        {
                            "collection": "users",
                            "action": "read",
                            "role": public_role["id"]
                        }
                    ]
                    
                    for permission in permissions:
                        try:
                            response = await client.post(f"{base_url}/permissions", json=permission, headers=headers)
                            print(f"  Oprávnění {permission['collection']}.{permission['action']}: {response.status_code}")
                        except Exception as e:
                            print(f"  Oprávnění {permission['collection']}.{permission['action']}: Exception - {e}")
                else:
                    print("WARNING: Public role nenalezena")
            else:
                print(f"WARNING: Nelze získat role - {response.status_code}")
            
            # 4. Kontrola výsledků
            print("\n5. Kontrola výsledků...")
            response = await client.get(f"{base_url}/collections", headers=headers)
            if response.status_code == 200:
                data = response.json()
                collections = data.get("data", [])
                
                our_collections = ["courses", "lessons", "user_progress", "achievements", "user_achievements", "users"]
                found = []
                
                for col in collections:
                    if col.get("collection") in our_collections:
                        found.append(col.get("collection"))
                
                print(f"Nalezené kolekce: {found}")
                
                if "users" in found:
                    print("SUCCESS: Users kolekce byla vytvořena!")
                    return True
                else:
                    print("WARNING: Users kolekce nebyla vytvořena")
                    return False
            else:
                print(f"ERROR: Kontrola selhala - {response.status_code}")
                return False
                
    except Exception as e:
        print(f"MAIN ERROR: {e}")
        return False

async def main():
    """Hlavní funkce"""
    success = await fix_directus_setup()
    
    if success:
        print("\nSUCCESS: Directus setup opraven!")
        print("\nDalší kroky:")
        print("1. Otevřete Directus admin: http://188.245.190.72:8057/admin")
        print("2. Zkontrolujte kolekci 'users' v Data Model")
        print("3. Zkontrolujte oprávnění v Access Policies")
        print("4. Restartujte aplikaci: python main.py")
        print("5. Otestujte registraci")
    else:
        print("\nERROR: Setup se nepodařil")
        print("\nMožná řešení:")
        print("1. Použijte manuální postup")
        print("2. Zkontrolujte Directus oprávnění")

if __name__ == "__main__":
    asyncio.run(main())
