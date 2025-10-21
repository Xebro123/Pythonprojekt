#!/usr/bin/env python3
"""
Kontrola existujících kolekcí v Directus
"""

import httpx
import asyncio
import json

async def check_existing_collections():
    """Kontrola existujících kolekcí"""
    base_url = "http://188.245.190.72:8057"
    email = "admin@ngc.com"
    password = "ngc_admin_789"
    
    print("Kontrola existujících kolekcí")
    print("=" * 40)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Přihlášení
            print("Přihlášení...")
            response = await client.post(f"{base_url}/auth/login", json={"email": email, "password": password})
            
            if response.status_code != 200:
                print(f"Chyba přihlášení: {response.status_code}")
                return
            
            data = response.json()
            token = data["data"]["access_token"]
            print(f"Token: {token[:30]}...")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Kontrola kolekcí
            print("\nKontrola kolekcí...")
            response = await client.get(f"{base_url}/collections", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                collections = data.get("data", [])
                print(f"Nalezené kolekce: {len(collections)}")
                
                for col in collections:
                    name = col.get("collection", "N/A")
                    meta = col.get("meta", {})
                    icon = meta.get("icon", "N/A")
                    note = meta.get("note", "N/A")
                    print(f"  - {name} (icon: {icon}, note: {note})")
                
                # Hledání našich kolekcí
                our_collections = ["courses", "lessons", "user_progress", "achievements", "user_achievements"]
                found = []
                missing = []
                
                for col in collections:
                    if col.get("collection") in our_collections:
                        found.append(col.get("collection"))
                
                for col in our_collections:
                    if col not in found:
                        missing.append(col)
                
                print(f"\nNaše kolekce:")
                print(f"  Nalezené: {found}")
                if missing:
                    print(f"  Chybí: {missing}")
                else:
                    print("  Všechny kolekce jsou přítomny!")
                
                if len(found) >= 3:  # Alespoň 3 z 5 kolekcí
                    print("\nSUCCESS: Kolekce byly úspěšně vytvořeny!")
                    print("Můžete pokračovat s aplikací.")
                    return True
                else:
                    print("\nWARNING: Některé kolekce chybí")
                    return False
            else:
                print(f"Chyba při získávání kolekcí: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"Chyba: {e}")
        return False

async def main():
    """Hlavní funkce"""
    success = await check_existing_collections()
    
    if success:
        print("\n🎉 Kolekce jsou připraveny!")
        print("\nDalší kroky:")
        print("1. Otevřete aplikaci: http://localhost:8000")
        print("2. Otestujte všechny funkce")
        print("3. Přidejte ukázková data do kolekcí")
    else:
        print("\n❌ Kolekce nejsou připraveny")
        print("\nMožná řešení:")
        print("1. Použijte manuální postup podle MANUAL_COLLECTIONS.md")
        print("2. Nebo zkuste opravit script")

if __name__ == "__main__":
    asyncio.run(main())
