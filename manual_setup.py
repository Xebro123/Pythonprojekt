#!/usr/bin/env python3
"""
Manuální setup Directus - pokud automatický nefunguje
"""

import httpx
import json
import asyncio
from typing import Dict, Any

# Konfigurace
DIRECTUS_URL = "http://188.245.190.72:8057"

class ManualDirectusSetup:
    def __init__(self):
        self.base_url = DIRECTUS_URL
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    async def test_connection(self):
        """Test připojení k Directus"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/server/ping")
                print(f"📡 Ping status: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Directus server je dostupný")
                    return True
                else:
                    print("❌ Directus server není dostupný")
                    return False
        except Exception as e:
            print(f"❌ Chyba připojení: {e}")
            return False
    
    async def get_server_info(self):
        """Získání informací o serveru"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/server/info")
                print(f"📊 Server info: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"📊 Directus verze: {data.get('data', {}).get('version', 'Neznámá')}")
                    return True
        except Exception as e:
            print(f"❌ Chyba: {e}")
        return False
    
    async def test_auth_endpoints(self):
        """Test různých auth endpointů"""
        endpoints = [
            "/auth/login",
            "/auth/authenticate", 
            "/login",
            "/admin/login",
            "/api/auth/login"
        ]
        
        print("\n🔍 Testování auth endpointů:")
        for endpoint in endpoints:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.base_url}{endpoint}",
                        json={"email": "test@test.com", "password": "test"}
                    )
                    print(f"  {endpoint}: {response.status_code}")
            except Exception as e:
                print(f"  {endpoint}: Chyba - {e}")
    
    def print_manual_instructions(self):
        """Vytiskne manuální instrukce"""
        print("\n" + "="*60)
        print("📋 MANUÁLNÍ SETUP INSTRUKCE")
        print("="*60)
        print("\n1. 🌐 Otevřete Directus admin panel:")
        print(f"   {self.base_url}/admin")
        print("\n2. 🔐 Přihlaste se s vašimi údaji")
        print("\n3. 📚 Vytvořte kolekce ručně:")
        print("   - Přejděte na Settings > Data Model")
        print("   - Klikněte 'Create Collection'")
        print("   - Vytvořte tyto kolekce:")
        print("     • courses")
        print("     • lessons") 
        print("     • user_progress")
        print("     • achievements")
        print("     • user_achievements")
        print("\n4. 🔑 Vytvořte API token:")
        print("   - Přejděte na Settings > Access Tokens")
        print("   - Klikněte 'Create Token'")
        print("   - Název: 'Python Kurz API'")
        print("   - Oprávnění: 'Full Access'")
        print("   - Zkopírujte token")
        print("\n5. 📝 Aktualizujte .env soubor:")
        print("   - Otevřete env.local")
        print("   - Nahraďte 'your-directus-token-here' vaším tokenem")
        print("   - Přejmenujte env.local na .env")
        print("\n6. 🚀 Spusťte aplikaci:")
        print("   python main.py")
        print("\n" + "="*60)

async def main():
    """Hlavní funkce"""
    print("🔧 Manuální Directus Setup")
    print("=" * 40)
    
    setup = ManualDirectusSetup()
    
    # Test připojení
    print("\n1. Testování připojení...")
    if not await setup.test_connection():
        print("❌ Nelze se připojit k Directus serveru")
        return
    
    # Server info
    print("\n2. Získávání informací o serveru...")
    await setup.get_server_info()
    
    # Test auth endpointů
    print("\n3. Testování auth endpointů...")
    await setup.test_auth_endpoints()
    
    # Manuální instrukce
    setup.print_manual_instructions()

if __name__ == "__main__":
    asyncio.run(main())
