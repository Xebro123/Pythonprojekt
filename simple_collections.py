#!/usr/bin/env python3
"""
Jednoduché vytvoření kolekcí v Directus
"""

import httpx
import asyncio

async def create_simple_collections():
    """Vytvoření jednoduchých kolekcí"""
    base_url = "http://188.245.190.72:8057"
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print("Vytváření jednoduchých kolekcí")
    print("=" * 40)
    
    try:
        async with httpx.AsyncClient() as client:
            # Přihlášení
            print("Přihlášení...")
            response = await client.post(
                f"{base_url}/auth/login",
                json={"email": email, "password": password}
            )
            
            if response.status_code != 200:
                print(f"Chyba přihlášení: {response.status_code}")
                return
            
            data = response.json()
            token = data["data"]["access_token"]
            print(f"Token: {token[:20]}...")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Vytvoření jednoduché kolekce
            print("\nVytváření kolekce 'courses'...")
            collection_data = {
                "collection": "courses",
                "meta": {
                    "collection": "courses",
                    "icon": "folder",
                    "note": "Kurzy programování"
                },
                "schema": {
                    "name": "courses"
                }
            }
            
            response = await client.post(
                f"{base_url}/collections",
                json=collection_data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code in [200, 201]:
                print("✅ Kolekce 'courses' vytvořena!")
            else:
                print(f"❌ Chyba: {response.text}")
            
            # Kontrola
            print("\nKontrola kolekcí...")
            response = await client.get(f"{base_url}/collections", headers=headers)
            if response.status_code == 200:
                data = response.json()
                collections = data.get("data", [])
                print(f"Nalezené kolekce: {len(collections)}")
                for col in collections:
                    print(f"  - {col.get('collection', 'N/A')}")
            else:
                print(f"Chyba kontroly: {response.status_code}")
                
    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    asyncio.run(create_simple_collections())
