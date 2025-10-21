#!/usr/bin/env python3
"""
Debug API volání pro Directus
"""

import httpx
import asyncio
import json

async def debug_directus_api():
    """Debug Directus API"""
    base_url = "http://188.245.190.72:8057"
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print("Debug Directus API")
    print("=" * 40)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 1. Přihlášení
            print("1. Přihlášení...")
            response = await client.post(f"{base_url}/auth/login", json={"email": email, "password": password})
            print(f"   Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"   Error: {response.text}")
                return
            
            data = response.json()
            token = data["data"]["access_token"]
            print(f"   Token: {token[:30]}...")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # 2. Test různých endpointů
            print("\n2. Testování endpointů...")
            
            endpoints = [
                "/collections",
                "/admin/collections", 
                "/api/collections",
                "/server/collections"
            ]
            
            for endpoint in endpoints:
                try:
                    response = await client.get(f"{base_url}{endpoint}", headers=headers)
                    print(f"   {endpoint}: {response.status_code}")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"     Data: {json.dumps(data, indent=2)[:200]}...")
                except Exception as e:
                    print(f"   {endpoint}: Exception - {e}")
            
            # 3. Zkusíme vytvořit kolekci s různými endpointy
            print("\n3. Testování vytvoření kolekce...")
            
            collection_data = {
                "collection": "debug_test",
                "meta": {
                    "collection": "debug_test",
                    "icon": "folder"
                }
            }
            
            create_endpoints = [
                "/collections",
                "/admin/collections",
                "/api/collections"
            ]
            
            for endpoint in create_endpoints:
                try:
                    print(f"   Zkouším {endpoint}...")
                    response = await client.post(f"{base_url}{endpoint}", json=collection_data, headers=headers)
                    print(f"     Status: {response.status_code}")
                    if response.status_code in [200, 201]:
                        print(f"     SUCCESS: Kolekce vytvořena!")
                        print(f"     Response: {response.text[:200]}...")
                        break
                    else:
                        print(f"     Error: {response.text[:200]}...")
                except Exception as e:
                    print(f"     Exception: {e}")
            
            # 4. Zkusíme GraphQL endpoint
            print("\n4. Testování GraphQL...")
            try:
                graphql_query = {
                    "query": "query { collections { collection } }"
                }
                response = await client.post(f"{base_url}/graphql", json=graphql_query, headers=headers)
                print(f"   GraphQL: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"     Data: {json.dumps(data, indent=2)[:200]}...")
            except Exception as e:
                print(f"   GraphQL Exception: {e}")
                
    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_directus_api())
