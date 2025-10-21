#!/usr/bin/env python3
"""
Vytvoření zbývajících kolekcí v Directus
"""

import httpx
import asyncio

async def create_remaining_collections():
    """Vytvoření zbývajících kolekcí"""
    base_url = "http://188.245.190.72:8057"
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print("Vytváření zbývajících kolekcí")
    print("=" * 40)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Přihlášení
            print("Přihlášení...")
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
            
            # Zbývající kolekce
            remaining_collections = [
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
            
            print("\nVytváření zbývajících kolekcí...")
            created_count = 0
            
            for collection in remaining_collections:
                print(f"\nVytváření: {collection['name']}")
                
                collection_data = {
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
                }
                
                try:
                    response = await client.post(
                        f"{base_url}/collections",
                        json=collection_data,
                        headers=headers
                    )
                    
                    print(f"  Status: {response.status_code}")
                    if response.status_code in [200, 201]:
                        print(f"  SUCCESS: {collection['name']} vytvořena!")
                        created_count += 1
                    else:
                        print(f"  ERROR: {response.text[:100]}...")
                        
                except Exception as e:
                    print(f"  EXCEPTION: {e}")
            
            # Kontrola výsledků
            print(f"\nVytvořeno: {created_count}/{len(remaining_collections)}")
            
            # Finální kontrola
            print("\nFinální kontrola...")
            response = await client.get(f"{base_url}/collections", headers=headers)
            if response.status_code == 200:
                data = response.json()
                collections = data.get("data", [])
                
                our_collections = ["courses", "lessons", "user_progress", "achievements", "user_achievements"]
                found = []
                
                for col in collections:
                    if col.get("collection") in our_collections:
                        found.append(col.get("collection"))
                
                print(f"Nalezené naše kolekce: {found}")
                
                if len(found) == len(our_collections):
                    print("SUCCESS: Všechny kolekce jsou připraveny!")
                    return True
                else:
                    missing = set(our_collections) - set(found)
                    print(f"WARNING: Chybí kolekce: {missing}")
                    return False
            else:
                print(f"ERROR: Kontrola selhala - {response.status_code}")
                return False
                
    except Exception as e:
        print(f"MAIN ERROR: {e}")
        return False

async def main():
    """Hlavní funkce"""
    success = await create_remaining_collections()
    
    if success:
        print("\n🎉 Všechny kolekce jsou připraveny!")
        print("\nDalší kroky:")
        print("1. Otevřete Directus admin: http://188.245.190.72:8057/admin")
        print("2. Zkontrolujte kolekce v Settings > Data Model")
        print("3. Přidejte pole do kolekcí")
        print("4. Nastavte oprávnění")
        print("5. Vytvořte API token")
        print("6. Spusťte aplikaci: python main.py")
    else:
        print("\n❌ Některé kolekce se nevytvořily")
        print("\nMožná řešení:")
        print("1. Použijte manuální postup podle MANUAL_COLLECTIONS.md")
        print("2. Nebo zkuste opravit script")

if __name__ == "__main__":
    asyncio.run(main())
