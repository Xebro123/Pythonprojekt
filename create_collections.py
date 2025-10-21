#!/usr/bin/env python3
"""
Vytvoření kolekcí v Directus s autentifikací
"""

import httpx
import asyncio
import json

async def create_collections():
    """Vytvoření kolekcí s autentifikací"""
    base_url = "http://188.245.190.72:8057"
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print("Vytváření kolekcí v Directus")
    print("=" * 50)
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Přihlášení
            print("1. Přihlášení...")
            response = await client.post(
                f"{base_url}/auth/login",
                json={"email": email, "password": password}
            )
            
            if response.status_code != 200:
                print(f"   Chyba přihlášení: {response.status_code}")
                print(f"   Response: {response.text}")
                return
            
            data = response.json()
            token = data["data"]["access_token"]
            print(f"   Token získán: {token[:20]}...")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # 2. Vytvoření kolekcí
            collections = [
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
            
            print("\n2. Vytváření kolekcí...")
            for collection in collections:
                print(f"   Vytváření: {collection['name']}")
                
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
                
                response = await client.post(
                    f"{base_url}/collections",
                    json=collection_data,
                    headers=headers
                )
                
                if response.status_code in [200, 201]:
                    print(f"     ✅ {collection['name']} vytvořena")
                else:
                    print(f"     ❌ Chyba {collection['name']}: {response.status_code}")
                    print(f"     Response: {response.text}")
            
            # 3. Kontrola vytvořených kolekcí
            print("\n3. Kontrola kolekcí...")
            response = await client.get(f"{base_url}/collections", headers=headers)
            if response.status_code == 200:
                data = response.json()
                collections = data.get("data", [])
                print(f"   Nalezené kolekce: {len(collections)}")
                for col in collections:
                    print(f"     - {col.get('collection', 'N/A')}")
            else:
                print(f"   Chyba při kontrole: {response.status_code}")
            
            print("\n✅ Setup dokončen!")
            print("\nDalší kroky:")
            print("1. Otevřete Directus admin: http://188.245.190.72:8057/admin")
            print("2. Zkontrolujte kolekce v Settings > Data Model")
            print("3. Přidejte pole do kolekcí")
            print("4. Nastavte oprávnění")
            
    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    asyncio.run(create_collections())
