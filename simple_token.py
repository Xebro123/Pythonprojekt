#!/usr/bin/env python3
"""
Jednoduché získání Directus tokenu
"""

import httpx
import asyncio
import json

async def get_token():
    """Získání tokenu"""
    base_url = "http://188.245.190.72:8057"
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print("Získávání Directus tokenu...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/auth/login",
                json={"email": email, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data["data"]["access_token"]
                print(f"Token získán: {token[:50]}...")
                
                # Uložení do .env
                with open("env.local", "r", encoding="utf-8") as f:
                    content = f.read()
                
                updated_content = content.replace("your-directus-token-here", token)
                
                with open(".env", "w", encoding="utf-8") as f:
                    f.write(updated_content)
                
                print("Token uložen do .env souboru")
                print("Můžete spustit aplikaci: python main.py")
                return token
            else:
                print(f"Chyba: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
    except Exception as e:
        print(f"Chyba: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(get_token())
