#!/usr/bin/env python3
"""
Automatický setup Directus kolekcí bez interaktivního vstupu
"""

import httpx
import asyncio
import json
from typing import Dict, Any

# Konfigurace
DIRECTUS_URL = "http://188.245.190.72:8057"

class AutoDirectusSetup:
    def __init__(self, token: str = None):
        self.base_url = DIRECTUS_URL
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}" if token else None
        }
    
    async def test_connection(self):
        """Test připojení"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/server/ping")
                print(f"Ping: {response.status_code}")
                return response.status_code == 200
        except Exception as e:
            print(f"Chyba připojení: {e}")
            return False
    
    async def create_collection_simple(self, collection_name: str) -> bool:
        """Jednoduché vytvoření kolekce"""
        try:
            async with httpx.AsyncClient() as client:
                # Základní kolekce
                collection_data = {
                    "collection": collection_name,
                    "meta": {
                        "collection": collection_name,
                        "icon": "folder",
                        "note": f"Kolekce {collection_name}",
                        "display_template": "{{title}}",
                        "hidden": False,
                        "singleton": False
                    },
                    "schema": {
                        "name": collection_name
                    }
                }
                
                print(f"Vytváření kolekce: {collection_name}")
                response = await client.post(
                    f"{self.base_url}/collections",
                    headers=self.headers,
                    json=collection_data
                )
                
                if response.status_code in [200, 201]:
                    print(f"Kolekce '{collection_name}' vytvořena")
                    return True
                else:
                    print(f"Chyba při vytváření '{collection_name}': {response.status_code}")
                    if response.text:
                        print(f"Response: {response.text[:200]}...")
                    return False
                    
        except Exception as e:
            print(f"Chyba: {e}")
            return False
    
    async def create_basic_fields(self, collection: str, fields: list) -> bool:
        """Vytvoření základních polí"""
        try:
            async with httpx.AsyncClient() as client:
                for field in fields:
                    try:
                        response = await client.post(
                            f"{self.base_url}/fields/{collection}",
                            headers=self.headers,
                            json=field
                        )
                        
                        if response.status_code in [200, 201]:
                            print(f"  Pole '{field['field']}' vytvořeno")
                        else:
                            print(f"  Chyba pole '{field['field']}': {response.status_code}")
                    except Exception as e:
                        print(f"  Chyba pole '{field['field']}': {e}")
                
                return True
        except Exception as e:
            print(f"Chyba při vytváření polí: {e}")
            return False
    
    async def setup_basic_collections(self):
        """Nastavení základních kolekcí"""
        
        # 1. Kurzy (courses)
        print("\n1. Vytváření kolekce 'courses'...")
        await self.create_collection_simple("courses")
        
        # Základní pole pro kurzy
        courses_fields = [
            {
                "field": "id",
                "type": "integer",
                "meta": {
                    "hidden": True,
                    "interface": "input",
                    "readonly": True
                },
                "schema": {
                    "is_primary_key": True,
                    "has_auto_increment": True
                }
            },
            {
                "field": "title",
                "type": "string",
                "meta": {
                    "interface": "input",
                    "display": "Název kurzu",
                    "required": True
                },
                "schema": {
                    "max_length": 200
                }
            },
            {
                "field": "description",
                "type": "text",
                "meta": {
                    "interface": "input-multiline",
                    "display": "Popis kurzu"
                }
            },
            {
                "field": "level",
                "type": "string",
                "meta": {
                    "interface": "input",
                    "display": "Úroveň"
                },
                "schema": {
                    "max_length": 50
                }
            }
        ]
        
        await self.create_basic_fields("courses", courses_fields)
        
        # 2. Lekce (lessons)
        print("\n2. Vytváření kolekce 'lessons'...")
        await self.create_collection_simple("lessons")
        
        # Základní pole pro lekce
        lessons_fields = [
            {
                "field": "id",
                "type": "integer",
                "meta": {
                    "hidden": True,
                    "interface": "input",
                    "readonly": True
                },
                "schema": {
                    "is_primary_key": True,
                    "has_auto_increment": True
                }
            },
            {
                "field": "title",
                "type": "string",
                "meta": {
                    "interface": "input",
                    "display": "Název lekce",
                    "required": True
                },
                "schema": {
                    "max_length": 200
                }
            },
            {
                "field": "description",
                "type": "text",
                "meta": {
                    "interface": "input-multiline",
                    "display": "Popis lekce"
                }
            },
            {
                "field": "content",
                "type": "text",
                "meta": {
                    "interface": "input-multiline",
                    "display": "Obsah lekce"
                }
            }
        ]
        
        await self.create_basic_fields("lessons", lessons_fields)
        
        # 3. Pokrok uživatelů (user_progress)
        print("\n3. Vytváření kolekce 'user_progress'...")
        await self.create_collection_simple("user_progress")
        
        # Základní pole pro pokrok
        progress_fields = [
            {
                "field": "id",
                "type": "integer",
                "meta": {
                    "hidden": True,
                    "interface": "input",
                    "readonly": True
                },
                "schema": {
                    "is_primary_key": True,
                    "has_auto_increment": True
                }
            },
            {
                "field": "user_id",
                "type": "string",
                "meta": {
                    "interface": "input",
                    "display": "ID uživatele"
                },
                "schema": {
                    "max_length": 100
                }
            },
            {
                "field": "lesson_id",
                "type": "integer",
                "meta": {
                    "interface": "input",
                    "display": "ID lekce"
                }
            },
            {
                "field": "completed",
                "type": "boolean",
                "meta": {
                    "interface": "boolean",
                    "display": "Dokončeno"
                },
                "schema": {
                    "default_value": False
                }
            }
        ]
        
        await self.create_basic_fields("user_progress", progress_fields)
        
        # 4. Achievementy (achievements)
        print("\n4. Vytváření kolekce 'achievements'...")
        await self.create_collection_simple("achievements")
        
        # Základní pole pro achievementy
        achievement_fields = [
            {
                "field": "id",
                "type": "integer",
                "meta": {
                    "hidden": True,
                    "interface": "input",
                    "readonly": True
                },
                "schema": {
                    "is_primary_key": True,
                    "has_auto_increment": True
                }
            },
            {
                "field": "name",
                "type": "string",
                "meta": {
                    "interface": "input",
                    "display": "Název",
                    "required": True
                },
                "schema": {
                    "max_length": 100
                }
            },
            {
                "field": "description",
                "type": "text",
                "meta": {
                    "interface": "input-multiline",
                    "display": "Popis"
                }
            },
            {
                "field": "points",
                "type": "integer",
                "meta": {
                    "interface": "input",
                    "display": "Body"
                },
                "schema": {
                    "default_value": 0
                }
            }
        ]
        
        await self.create_basic_fields("achievements", achievement_fields)
        
        print("\nZákladní kolekce byly vytvořeny!")
        print("\nDalší kroky:")
        print("1. Otevřete Directus admin panel: http://188.245.190.72:8057/admin")
        print("2. Zkontrolujte vytvořené kolekce")
        print("3. Přidejte další pole podle potřeby")
        print("4. Vytvořte API token pro aplikaci")

async def main():
    """Hlavní funkce"""
    print("Automatický Directus Setup")
    print("=" * 50)
    
    # Test bez tokenu
    setup = AutoDirectusSetup()
    
    # Test připojení
    print("\n1. Testování připojení...")
    if not await setup.test_connection():
        print("Nelze se připojit k Directus serveru")
        return
    
    # Vytvoření základních kolekcí
    print("\n2. Vytváření základních kolekcí...")
    await setup.setup_basic_collections()
    
    print("\nSetup dokončen!")

if __name__ == "__main__":
    asyncio.run(main())
