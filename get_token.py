#!/usr/bin/env python3
"""
Získání Directus tokenu přes přihlášení
"""

import httpx
import asyncio
import json

async def get_directus_token():
    """Získání tokenu přes přihlášení"""
    base_url = "http://188.245.190.72:8057"
    
    # Vaše admin údaje
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print("Získávání Directus tokenu")
    print("=" * 40)
    
    try:
        async with httpx.AsyncClient() as client:
            # Zkusíme různé endpointy pro přihlášení
            endpoints = [
                "/auth/login",
                "/auth/authenticate", 
                "/login",
                "/admin/login"
            ]
            
            for endpoint in endpoints:
                try:
                    print(f"Zkouším endpoint: {endpoint}")
                    
                    # Různé formáty dat
                    data_formats = [
                        {"email": email, "password": password},
                        {"username": email, "password": password},
                        {"user": email, "password": password}
                    ]
                    
                    for data_format in data_formats:
                        try:
                            response = await client.post(
                                f"{base_url}{endpoint}",
                                json=data_format
                            )
                            
                            print(f"  Status: {response.status_code}")
                            
                            if response.status_code == 200:
                                data = response.json()
                                print(f"  Úspěch! Response: {json.dumps(data, indent=2)[:300]}...")
                                
                                # Hledání tokenu v různých strukturách
                                token = None
                                if "data" in data and "access_token" in data["data"]:
                                    token = data["data"]["access_token"]
                                elif "access_token" in data:
                                    token = data["access_token"]
                                elif "token" in data:
                                    token = data["token"]
                                elif "data" in data and "token" in data["data"]:
                                    token = data["data"]["token"]
                                
                                if token:
                                    print(f"\n✅ Token nalezen: {token[:20]}...")
                                    
                                    # Test tokenu
                                    await test_token(base_url, token)
                                    return token
                                else:
                                    print("  Token nenalezen v odpovědi")
                            else:
                                print(f"  Chyba: {response.status_code}")
                                if response.text:
                                    print(f"  Response: {response.text[:200]}...")
                                    
                        except Exception as e:
                            print(f"  Chyba s datovým formátem: {e}")
                            continue
                            
                except Exception as e:
                    print(f"Chyba s endpointem {endpoint}: {e}")
                    continue
            
            print("\n❌ Nepodařilo se získat token")
            return None
            
    except Exception as e:
        print(f"Chyba připojení: {e}")
        return None

async def test_token(base_url: str, token: str):
    """Test tokenu"""
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Test server info
            response = await client.get(f"{base_url}/server/info", headers=headers)
            print(f"Token test - Server info: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Token funguje!")
                
                # Test kolekcí
                try:
                    response = await client.get(f"{base_url}/collections", headers=headers)
                    print(f"Token test - Collections: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        collections = data.get("data", [])
                        print(f"✅ Nalezeno {len(collections)} kolekcí")
                        
                        # Hledání našich kolekcí
                        our_collections = ["courses", "lessons", "user_progress", "achievements"]
                        found = [c for c in collections if c.get("collection") in our_collections]
                        print(f"✅ Naše kolekce: {[c['collection'] for c in found]}")
                    else:
                        print(f"❌ Chyba při získávání kolekcí: {response.status_code}")
                        
                except Exception as e:
                    print(f"Chyba při testování kolekcí: {e}")
            else:
                print(f"❌ Token nefunguje: {response.status_code}")
                
    except Exception as e:
        print(f"Chyba při testování tokenu: {e}")

async def save_token_to_env(token: str):
    """Uložení tokenu do .env souboru"""
    try:
        # Přečteme env.local
        with open("env.local", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Nahradíme token
        updated_content = content.replace("your-directus-token-here", token)
        
        # Uložíme do .env
        with open(".env", "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        print(f"✅ Token uložen do .env souboru")
        
    except Exception as e:
        print(f"❌ Chyba při ukládání tokenu: {e}")

async def main():
    """Hlavní funkce"""
    print("Directus Token Generator")
    print("=" * 50)
    
    # Získání tokenu
    token = await get_directus_token()
    
    if token:
        # Uložení tokenu
        await save_token_to_env(token)
        
        print(f"\n🎉 Úspěch!")
        print(f"Token: {token[:20]}...")
        print(f"Token uložen do .env souboru")
        print(f"\nMůžete spustit aplikaci: python main.py")
    else:
        print(f"\n❌ Nepodařilo se získat token")
        print(f"\nMožná řešení:")
        print(f"1. Zkontrolujte admin údaje")
        print(f"2. Ověřte, že máte admin oprávnění")
        print(f"3. Zkuste se přihlásit přes webové rozhraní")
        print(f"4. Zkontrolujte Directus konfiguraci")

if __name__ == "__main__":
    asyncio.run(main())
