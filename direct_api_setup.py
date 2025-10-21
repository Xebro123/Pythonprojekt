#!/usr/bin/env python3
"""
Přímé API volání pro vytvoření Directus kolekcí
"""

import httpx
import asyncio
import json
from typing import Dict, Any

# Konfigurace
DIRECTUS_URL = "http://188.245.190.72:8057"

class DirectAPISetup:
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
    
    async def create_collection_direct(self, collection_name: str, fields: list) -> bool:
        """Přímé vytvoření kolekce přes API"""
        try:
            async with httpx.AsyncClient() as client:
                # Vytvoření kolekce
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
                    
                    # Přidání polí
                    for field in fields:
                        await self.create_field(collection_name, field)
                    
                    return True
                else:
                    print(f"Chyba při vytváření '{collection_name}': {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"Chyba: {e}")
            return False
    
    async def create_field(self, collection: str, field: Dict[str, Any]) -> bool:
        """Vytvoření pole v kolekci"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/fields/{collection}",
                    headers=self.headers,
                    json=field
                )
                
                if response.status_code in [200, 201]:
                    print(f"  Pole '{field['field']}' vytvořeno")
                    return True
                else:
                    print(f"  Chyba pole '{field['field']}': {response.status_code}")
                    return False
        except Exception as e:
            print(f"  Chyba pole: {e}")
            return False
    
    async def setup_all_collections(self):
        """Nastavení všech kolekcí"""
        
        # 1. Kurzy (courses)
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
                "field": "course_id",
                "type": "string",
                "meta": {
                    "interface": "input",
                    "display": "Course ID",
                    "required": True
                },
                "schema": {
                    "is_unique": True,
                    "max_length": 50
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
                    "interface": "select-dropdown",
                    "display": "Úroveň",
                    "options": {
                        "choices": [
                            {"text": "Úvod", "value": "uvod"},
                            {"text": "Základy", "value": "zaklady"},
                            {"text": "Pokročilé", "value": "pokrocile"}
                        ]
                    }
                },
                "schema": {
                    "max_length": 50
                }
            },
            {
                "field": "status",
                "type": "string",
                "meta": {
                    "interface": "select-dropdown",
                    "display": "Status",
                    "options": {
                        "choices": [
                            {"text": "Publikováno", "value": "published"},
                            {"text": "Koncept", "value": "draft"}
                        ]
                    }
                },
                "schema": {
                    "default_value": "draft",
                    "max_length": 20
                }
            },
            {
                "field": "sort",
                "type": "integer",
                "meta": {
                    "interface": "input",
                    "display": "Pořadí"
                },
                "schema": {
                    "default_value": 0
                }
            }
        ]
        
        await self.create_collection_direct("courses", courses_fields)
        
        # 2. Lekce (lessons)
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
                "field": "course",
                "type": "integer",
                "meta": {
                    "interface": "select-dropdown-m2o",
                    "display": "Kurz",
                    "required": True
                },
                "schema": {
                    "is_foreign_key": True,
                    "foreign_key_table": "courses"
                }
            },
            {
                "field": "lesson_number",
                "type": "integer",
                "meta": {
                    "interface": "input",
                    "display": "Číslo lekce",
                    "required": True
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
                    "interface": "input-rich-text-html",
                    "display": "Obsah lekce"
                }
            },
            {
                "field": "code_example",
                "type": "text",
                "meta": {
                    "interface": "input-code",
                    "display": "Příklad kódu",
                    "options": {
                        "language": "python"
                    }
                }
            },
            {
                "field": "status",
                "type": "string",
                "meta": {
                    "interface": "select-dropdown",
                    "display": "Status",
                    "options": {
                        "choices": [
                            {"text": "Publikováno", "value": "published"},
                            {"text": "Koncept", "value": "draft"}
                        ]
                    }
                },
                "schema": {
                    "default_value": "draft",
                    "max_length": 20
                }
            },
            {
                "field": "sort",
                "type": "integer",
                "meta": {
                    "interface": "input",
                    "display": "Pořadí"
                },
                "schema": {
                    "default_value": 0
                }
            }
        ]
        
        await self.create_collection_direct("lessons", lessons_fields)
        
        # 3. Pokrok uživatelů (user_progress)
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
                "field": "user",
                "type": "uuid",
                "meta": {
                    "interface": "select-dropdown-m2o",
                    "display": "Uživatel",
                    "required": True
                },
                "schema": {
                    "is_foreign_key": True,
                    "foreign_key_table": "directus_users"
                }
            },
            {
                "field": "lesson",
                "type": "integer",
                "meta": {
                    "interface": "select-dropdown-m2o",
                    "display": "Lekce",
                    "required": True
                },
                "schema": {
                    "is_foreign_key": True,
                    "foreign_key_table": "lessons"
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
            },
            {
                "field": "completion_percentage",
                "type": "float",
                "meta": {
                    "interface": "slider",
                    "display": "Procento dokončení",
                    "options": {
                        "min": 0,
                        "max": 100,
                        "step": 1
                    }
                },
                "schema": {
                    "default_value": 0.0
                }
            },
            {
                "field": "time_spent",
                "type": "integer",
                "meta": {
                    "interface": "input",
                    "display": "Čas strávený (sekundy)"
                },
                "schema": {
                    "default_value": 0
                }
            },
            {
                "field": "completed_at",
                "type": "datetime",
                "meta": {
                    "interface": "datetime",
                    "display": "Dokončeno dne"
                }
            }
        ]
        
        await self.create_collection_direct("user_progress", progress_fields)
        
        # 4. Achievementy (achievements)
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
                    "is_unique": True,
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
                "field": "icon",
                "type": "string",
                "meta": {
                    "interface": "input",
                    "display": "Ikona (FontAwesome)"
                },
                "schema": {
                    "max_length": 100
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
            },
            {
                "field": "condition_type",
                "type": "string",
                "meta": {
                    "interface": "select-dropdown",
                    "display": "Typ podmínky",
                    "options": {
                        "choices": [
                            {"text": "Dokončené lekce", "value": "lessons_completed"},
                            {"text": "Strávený čas", "value": "time_spent"},
                            {"text": "Perfektní skóre", "value": "perfect_score"}
                        ]
                    }
                },
                "schema": {
                    "max_length": 50
                }
            },
            {
                "field": "condition_value",
                "type": "integer",
                "meta": {
                    "interface": "input",
                    "display": "Hodnota podmínky"
                }
            },
            {
                "field": "status",
                "type": "string",
                "meta": {
                    "interface": "select-dropdown",
                    "display": "Status",
                    "options": {
                        "choices": [
                            {"text": "Publikováno", "value": "published"},
                            {"text": "Koncept", "value": "draft"}
                        ]
                    }
                },
                "schema": {
                    "default_value": "draft",
                    "max_length": 20
                }
            }
        ]
        
        await self.create_collection_direct("achievements", achievement_fields)
        
        # 5. Uživatelské achievementy (user_achievements)
        user_achievement_fields = [
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
                "field": "user",
                "type": "uuid",
                "meta": {
                    "interface": "select-dropdown-m2o",
                    "display": "Uživatel",
                    "required": True
                },
                "schema": {
                    "is_foreign_key": True,
                    "foreign_key_table": "directus_users"
                }
            },
            {
                "field": "achievement",
                "type": "integer",
                "meta": {
                    "interface": "select-dropdown-m2o",
                    "display": "Achievement",
                    "required": True
                },
                "schema": {
                    "is_foreign_key": True,
                    "foreign_key_table": "achievements"
                }
            },
            {
                "field": "earned_at",
                "type": "datetime",
                "meta": {
                    "interface": "datetime",
                    "display": "Získáno dne"
                },
                "schema": {
                    "default_value": "CURRENT_TIMESTAMP"
                }
            }
        ]
        
        await self.create_collection_direct("user_achievements", user_achievement_fields)
        
        print("\nVšechny kolekce byly úspěšně vytvořeny!")

async def main():
    """Hlavní funkce"""
    print("Directus API Setup")
    print("=" * 50)
    
    # Získání tokenu
    token = input("Zadejte Directus API token (nebo Enter pro test bez tokenu): ").strip()
    
    if not token:
        print("Testování bez tokenu (možná omezená funkcionalita)")
        token = None
    
    setup = DirectAPISetup(token)
    
    # Test připojení
    print("\n1. Testování připojení...")
    if not await setup.test_connection():
        print("Nelze se připojit k Directus serveru")
        return
    
    # Vytvoření kolekcí
    print("\n2. Vytváření kolekcí...")
    await setup.setup_all_collections()
    
    print("\nSetup dokončen!")
    print("\nDalší kroky:")
    print("1. Zkontrolujte kolekce v Directus admin panelu")
    print("2. Nastavte oprávnění pro Public a Authenticated role")
    print("3. Přidejte ukázková data")
    print("4. Spusťte aplikaci: python main.py")

if __name__ == "__main__":
    asyncio.run(main())
