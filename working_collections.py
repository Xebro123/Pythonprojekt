#!/usr/bin/env python3
"""
Funkční script pro vytvoření kolekcí v Directus
"""

import httpx
import asyncio
import json

async def create_working_collections():
    """Funkční vytvoření kolekcí"""
    base_url = "http://188.245.190.72:8057"
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print("Funkční vytváření kolekcí v Directus")
    print("=" * 50)
    
    try:
        # Větší timeout a retry mechanismus
        timeout = httpx.Timeout(60.0, connect=10.0, read=30.0, write=10.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            # 1. Přihlášení
            print("1. Přihlášení...")
            login_data = {"email": email, "password": password}
            
            try:
                response = await client.post(f"{base_url}/auth/login", json=login_data)
                print(f"   Login status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"   Login error: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"   Login exception: {e}")
                return False
            
            data = response.json()
            token = data["data"]["access_token"]
            print(f"   Token: {token[:30]}...")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # 2. Test připojení
            print("\n2. Test připojení...")
            try:
                response = await client.get(f"{base_url}/server/info", headers=headers)
                print(f"   Server info: {response.status_code}")
            except Exception as e:
                print(f"   Server info error: {e}")
                return False
            
            # 3. Vytvoření jedné testovací kolekce
            print("\n3. Vytváření testovací kolekce...")
            
            # Minimální formát dat
            collection_data = {
                "collection": "test_courses",
                "meta": {
                    "collection": "test_courses",
                    "icon": "folder",
                    "note": "Test kolekce pro kurzy"
                }
            }
            
            try:
                response = await client.post(
                    f"{base_url}/collections",
                    json=collection_data,
                    headers=headers
                )
                
                print(f"   Status: {response.status_code}")
                if response.status_code in [200, 201]:
                    print("   SUCCESS: Test kolekce vytvořena!")
                    
                    # Kontrola
                    print("\n4. Kontrola kolekcí...")
                    response = await client.get(f"{base_url}/collections", headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        collections = data.get("data", [])
                        print(f"   Celkem kolekcí: {len(collections)}")
                        
                        # Hledání naší kolekce
                        found = False
                        for col in collections:
                            if col.get("collection") == "test_courses":
                                found = True
                                print(f"   NALEZENA: {col.get('collection')}")
                                break
                        
                        if found:
                            print("   SUCCESS: Kolekce byla úspěšně vytvořena a nalezena!")
                            return True
                        else:
                            print("   WARNING: Kolekce se nevytvořila nebo není viditelná")
                            return False
                    else:
                        print(f"   ERROR: Kontrola selhala - {response.status_code}")
                        return False
                else:
                    print(f"   ERROR: Vytvoření selhalo - {response.status_code}")
                    print(f"   Response: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"   ERROR: Exception při vytváření - {e}")
                return False
                
    except Exception as e:
        print(f"MAIN ERROR: {e}")
        return False

async def main():
    """Hlavní funkce"""
    print("Spouštění funkčního scriptu...")
    success = await create_working_collections()
    
    if success:
        print("\nSUCCESS: Script funguje!")
        print("\nDalší kroky:")
        print("1. Script dokáže vytvářet kolekce")
        print("2. Můžeme rozšířit o všechny potřebné kolekce")
        print("3. Nebo použít manuální postup")
    else:
        print("\nERROR: Script nefunguje")
        print("\nMožná řešení:")
        print("1. Zkontrolujte Directus server")
        print("2. Ověřte admin údaje")
        print("3. Použijte manuální postup")

if __name__ == "__main__":
    asyncio.run(main())
