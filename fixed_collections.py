#!/usr/bin/env python3
"""
Opravený script pro vytvoření kolekcí v Directus
"""

import httpx
import asyncio
import json

async def create_collections_fixed():
    """Opravené vytvoření kolekcí"""
    base_url = "http://188.245.190.72:8057"
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print("Opravené vytváření kolekcí v Directus")
    print("=" * 50)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 1. Přihlášení
            print("1. Přihlášení...")
            login_data = {"email": email, "password": password}
            response = await client.post(f"{base_url}/auth/login", json=login_data)
            
            print(f"   Login status: {response.status_code}")
            if response.status_code != 200:
                print(f"   Login error: {response.text}")
                return False
            
            data = response.json()
            token = data["data"]["access_token"]
            print(f"   Token: {token[:30]}...")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # 2. Test připojení s tokenem
            print("\n2. Test připojení s tokenem...")
            response = await client.get(f"{base_url}/server/info", headers=headers)
            print(f"   Server info: {response.status_code}")
            
            # 3. Vytvoření kolekcí - zkusíme různé formáty
            collections_to_create = [
                {
                    "name": "courses",
                    "display": "Kurzy",
                    "icon": "school",
                    "note": "Kurzy programování"
                },
                {
                    "name": "lessons",
                    "display": "Lekce", 
                    "icon": "book",
                    "note": "Lekce kurzů"
                },
                {
                    "name": "user_progress",
                    "display": "Pokrok uživatelů",
                    "icon": "trending_up",
                    "note": "Pokrok uživatelů v lekcích"
                },
                {
                    "name": "achievements",
                    "display": "Odměny",
                    "icon": "emoji_events", 
                    "note": "Odměny a úspěchy"
                },
                {
                    "name": "user_achievements",
                    "display": "Uživatelské odměny",
                    "icon": "star",
                    "note": "Získané odměny uživatelů"
                }
            ]
            
            print("\n3. Vytváření kolekcí...")
            created_count = 0
            
            for collection in collections_to_create:
                print(f"\n   Vytváření: {collection['name']}")
                
                # Zkusíme různé formáty dat
                formats_to_try = [
                    # Formát 1: Základní
                    {
                        "collection": collection["name"],
                        "meta": {
                            "collection": collection["name"],
                            "icon": collection["icon"],
                            "note": collection["note"],
                            "display_template": "{{title}}",
                            "hidden": False,
                            "singleton": False
                        },
                        "schema": {
                            "name": collection["name"]
                        }
                    },
                    # Formát 2: Zjednodušený
                    {
                        "collection": collection["name"],
                        "meta": {
                            "collection": collection["name"],
                            "icon": collection["icon"],
                            "note": collection["note"]
                        }
                    },
                    # Formát 3: Minimální
                    {
                        "collection": collection["name"],
                        "meta": {
                            "collection": collection["name"]
                        }
                    }
                ]
                
                success = False
                for i, format_data in enumerate(formats_to_try):
                    try:
                        print(f"     Zkouším formát {i+1}...")
                        response = await client.post(
                            f"{base_url}/collections",
                            json=format_data,
                            headers=headers
                        )
                        
                        print(f"     Status: {response.status_code}")
                        if response.status_code in [200, 201]:
                            print(f"     ✅ {collection['name']} vytvořena!")
                            created_count += 1
                            success = True
                            break
                        else:
                            print(f"     ❌ Chyba: {response.text[:100]}...")
                            
                    except Exception as e:
                        print(f"     ❌ Exception: {e}")
                        continue
                
                if not success:
                    print(f"     ❌ Všechny formáty selhaly pro {collection['name']}")
            
            # 4. Kontrola výsledků
            print(f"\n4. Kontrola výsledků...")
            print(f"   Vytvořeno kolekcí: {created_count}/{len(collections_to_create)}")
            
            response = await client.get(f"{base_url}/collections", headers=headers)
            if response.status_code == 200:
                data = response.json()
                collections = data.get("data", [])
                print(f"   Celkem kolekcí v systému: {len(collections)}")
                
                # Hledání našich kolekcí
                our_collections = [c["name"] for c in collections_to_create]
                found_collections = []
                for col in collections:
                    if col.get("collection") in our_collections:
                        found_collections.append(col.get("collection"))
                
                print(f"   Naše kolekce nalezené: {found_collections}")
                
                if len(found_collections) == len(our_collections):
                    print("   ✅ Všechny kolekce byly úspěšně vytvořeny!")
                    return True
                else:
                    print(f"   ⚠️  Chybí kolekce: {set(our_collections) - set(found_collections)}")
                    return False
            else:
                print(f"   ❌ Chyba při kontrole: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Hlavní chyba: {e}")
        return False

async def main():
    """Hlavní funkce"""
    success = await create_collections_fixed()
    
    if success:
        print("\n🎉 Úspěch! Kolekce byly vytvořeny.")
        print("\nDalší kroky:")
        print("1. Otevřete Directus admin: http://188.245.190.72:8057/admin")
        print("2. Zkontrolujte kolekce v Settings > Data Model")
        print("3. Přidejte pole do kolekcí")
        print("4. Nastavte oprávnění")
        print("5. Vytvořte API token")
    else:
        print("\n❌ Některé kolekce se nevytvořily.")
        print("\nAlternativní řešení:")
        print("1. Použijte manuální postup podle MANUAL_COLLECTIONS.md")
        print("2. Nebo zkuste opravit script podle chybových zpráv")

if __name__ == "__main__":
    asyncio.run(main())
