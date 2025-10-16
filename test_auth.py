#!/usr/bin/env python3
"""
Test přihlášení do Directus s vašimi údaji
"""

import httpx
import asyncio

async def test_login():
    """Test přihlášení"""
    base_url = "http://188.245.190.72:8057"
    
    # Vaše údaje
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print(f"🔐 Testování přihlášení pro {email}")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # Test /admin/login endpoint
        try:
            print("🔍 Testování /admin/login...")
            response = await client.post(
                f"{base_url}/admin/login",
                json={"email": email, "password": password}
            )
            
            print(f"📊 Status: {response.status_code}")
            print(f"📊 Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Přihlášení úspěšné!")
                print(f"📊 Data: {data}")
                
                # Zkusíme najít token
                if "data" in data and "access_token" in data["data"]:
                    token = data["data"]["access_token"]
                    print(f"🔑 Token: {token[:20]}...")
                    return token
                elif "access_token" in data:
                    token = data["access_token"]
                    print(f"🔑 Token: {token[:20]}...")
                    return token
                else:
                    print("❌ Token nenalezen v odpovědi")
                    return None
            else:
                print(f"❌ Chyba přihlášení: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Chyba: {e}")
            return None

async def test_api_with_token(token):
    """Test API s tokenem"""
    if not token:
        print("❌ Žádný token k testování")
        return
    
    base_url = "http://188.245.190.72:8057"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"\n🔍 Testování API s tokenem...")
    
    async with httpx.AsyncClient() as client:
        try:
            # Test server info
            response = await client.get(f"{base_url}/server/info", headers=headers)
            print(f"📊 Server info: {response.status_code}")
            if response.status_code == 200:
                print("✅ API token funguje!")
                return True
            else:
                print(f"❌ API token nefunguje: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Chyba API testu: {e}")
            return False

async def main():
    """Hlavní funkce"""
    print("🧪 Test Directus přihlášení")
    print("=" * 40)
    
    # Test přihlášení
    token = await test_login()
    
    if token:
        # Test API
        await test_api_with_token(token)
        
        print(f"\n✅ Úspěch! Token: {token[:20]}...")
        print(f"\n📝 Zkopírujte tento token do env.local:")
        print(f"DIRECTUS_TOKEN={token}")
    else:
        print("\n❌ Přihlášení selhalo")
        print("\n🔧 Možná řešení:")
        print("1. Zkontrolujte email a heslo")
        print("2. Ověřte, že máte admin oprávnění")
        print("3. Zkuste se přihlásit přes webové rozhraní")

if __name__ == "__main__":
    asyncio.run(main())
