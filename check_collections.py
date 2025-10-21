#!/usr/bin/env python3
"""
Kontrola vytvořených kolekcí v Directus
"""

import httpx
import asyncio

async def check_collections():
    """Kontrola kolekcí"""
    base_url = "http://188.245.190.72:8057"
    
    print("Kontrola Directus kolekcí")
    print("=" * 40)
    
    try:
        async with httpx.AsyncClient() as client:
            # Test připojení
            response = await client.get(f"{base_url}/server/ping")
            print(f"Ping: {response.status_code}")
            
            if response.status_code != 200:
                print("Directus server není dostupný")
                return
            
            # Získání seznamu kolekcí
            try:
                response = await client.get(f"{base_url}/collections")
                print(f"Collections API: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    collections = data.get("data", [])
                    print(f"\nNalezené kolekce ({len(collections)}):")
                    
                    for collection in collections:
                        name = collection.get("collection", "N/A")
                        print(f"  - {name}")
                    
                    # Kontrola našich kolekcí
                    our_collections = ["courses", "lessons", "user_progress", "achievements"]
                    found = []
                    missing = []
                    
                    for col in our_collections:
                        if any(c.get("collection") == col for c in collections):
                            found.append(col)
                        else:
                            missing.append(col)
                    
                    print(f"\nNaše kolekce:")
                    print(f"  Nalezené: {found}")
                    if missing:
                        print(f"  Chybí: {missing}")
                    else:
                        print("  Všechny kolekce byly úspěšně vytvořeny!")
                        
                else:
                    print(f"Chyba při získávání kolekcí: {response.status_code}")
                    print(f"Response: {response.text}")
                    
            except Exception as e:
                print(f"Chyba při kontrole kolekcí: {e}")
                
    except Exception as e:
        print(f"Chyba připojení: {e}")

async def main():
    await check_collections()
    
    print("\nDalší kroky:")
    print("1. Otevřete Directus admin panel: http://188.245.190.72:8057/admin")
    print("2. Přihlaste se s vašimi údaji")
    print("3. Zkontrolujte kolekce v Settings > Data Model")
    print("4. Vytvořte API token pro aplikaci")

if __name__ == "__main__":
    asyncio.run(main())
