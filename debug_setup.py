#!/usr/bin/env python3
"""
Debug setup pro Directus kolekce
"""

import httpx
import asyncio
import json

async def debug_directus():
    """Debug Directus připojení a vytvoření kolekcí"""
    base_url = "http://188.245.190.72:8057"
    
    print("Debug Directus Setup")
    print("=" * 50)
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Test připojení
            print("1. Testování připojení...")
            response = await client.get(f"{base_url}/server/ping")
            print(f"   Ping: {response.status_code}")
            
            if response.status_code != 200:
                print("   ❌ Directus server není dostupný")
                return
            
            # 2. Test server info
            print("\n2. Testování server info...")
            response = await client.get(f"{base_url}/server/info")
            print(f"   Server info: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Directus verze: {data.get('data', {}).get('version', 'Neznámá')}")
            
            # 3. Test kolekcí (bez tokenu)
            print("\n3. Testování kolekcí (bez tokenu)...")
            response = await client.get(f"{base_url}/collections")
            print(f"   Collections: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                collections = data.get("data", [])
                print(f"   Nalezené kolekce: {len(collections)}")
                for col in collections:
                    print(f"     - {col.get('collection', 'N/A')}")
            else:
                print(f"   Chyba: {response.text}")
            
            # 4. Zkusíme vytvořit kolekci bez tokenu
            print("\n4. Testování vytvoření kolekce (bez tokenu)...")
            collection_data = {
                "collection": "test_collection",
                "meta": {
                    "collection": "test_collection",
                    "icon": "folder",
                    "note": "Test kolekce",
                    "display_template": "{{title}}",
                    "hidden": False,
                    "singleton": False
                },
                "schema": {
                    "name": "test_collection"
                }
            }
            
            response = await client.post(
                f"{base_url}/collections",
                json=collection_data
            )
            print(f"   Vytvoření kolekce: {response.status_code}")
            if response.status_code in [200, 201]:
                print("   ✅ Kolekce vytvořena bez tokenu!")
            else:
                print(f"   ❌ Chyba: {response.text}")
            
            # 5. Zkusíme získat token
            print("\n5. Testování získání tokenu...")
            response = await client.post(
                f"{base_url}/auth/login",
                json={"email": "admin@ngc.com", "password": "ngc_admin_789"}
            )
            print(f"   Login: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                token = data["data"]["access_token"]
                print(f"   ✅ Token získán: {token[:20]}...")
                
                # Test s tokenem
                print("\n6. Testování s tokenem...")
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.get(f"{base_url}/collections", headers=headers)
                print(f"   Collections s tokenem: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    collections = data.get("data", [])
                    print(f"   Nalezené kolekce: {len(collections)}")
                    for col in collections:
                        print(f"     - {col.get('collection', 'N/A')}")
                
                # Vytvoření kolekce s tokenem
                print("\n7. Vytvoření kolekce s tokenem...")
                response = await client.post(
                    f"{base_url}/collections",
                    json=collection_data,
                    headers=headers
                )
                print(f"   Vytvoření s tokenem: {response.status_code}")
                if response.status_code in [200, 201]:
                    print("   ✅ Kolekce vytvořena s tokenem!")
                else:
                    print(f"   ❌ Chyba: {response.text}")
            else:
                print(f"   ❌ Chyba přihlášení: {response.text}")
                
    except Exception as e:
        print(f"❌ Chyba: {e}")

if __name__ == "__main__":
    asyncio.run(debug_directus())
