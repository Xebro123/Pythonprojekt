#!/usr/bin/env python3
"""
Rychlý setup script pro Directus
"""

import asyncio
import sys
import os

# Přidání aktuálního adresáře do Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from setup_directus import DirectusSetup

async def quick_setup():
    """Rychlý setup"""
    print("🚀 Rychlý Directus Setup")
    print("=" * 30)
    
    # Získání admin údajů
    admin_email = input("Admin email (default: admin@example.com): ").strip()
    if not admin_email:
        admin_email = "admin@example.com"
    
    admin_password = input("Admin password (default: admin123): ").strip()
    if not admin_password:
        admin_password = "admin123"
    
    # Nastavení údajů
    setup = DirectusSetup()
    setup.ADMIN_EMAIL = admin_email
    setup.ADMIN_PASSWORD = admin_password
    
    # Přihlášení
    print(f"\n🔐 Přihlašování jako {admin_email}...")
    if not await setup.authenticate():
        print("❌ Chyba přihlášení. Zkontrolujte údaje.")
        return False
    
    # Vytvoření kolekcí
    print("\n📚 Vytváření kolekcí...")
    await setup.setup_collections()
    
    # Vytvoření ukázkových dat
    print("\n📝 Vytváření ukázkových dat...")
    await setup.create_sample_data()
    
    print("\n✅ Setup dokončen!")
    print("\n📋 Další kroky:")
    print("1. Přejděte na http://188.245.190.72:8057/admin")
    print("2. Vytvořte Directus token v Settings > Access Tokens")
    print("3. Zkopírujte token do env.local souboru")
    print("4. Spusťte aplikaci: python main.py")
    
    return True

if __name__ == "__main__":
    try:
        asyncio.run(quick_setup())
    except KeyboardInterrupt:
        print("\n❌ Setup přerušen uživatelem")
    except Exception as e:
        print(f"\n❌ Chyba: {e}")
