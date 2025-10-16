#!/usr/bin/env python3
"""
Automatický setup Directus kolekcí pro Python Kurz
"""

import httpx
import json
import asyncio
from typing import Dict, Any

# Konfigurace
DIRECTUS_URL = "http://188.245.190.72:8057"
ADMIN_EMAIL = "admin@example.com"  # Změňte na vaše admin údaje
ADMIN_PASSWORD = "admin123"  # Změňte na vaše heslo

class DirectusSetup:
    def __init__(self):
        self.base_url = DIRECTUS_URL
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    async def authenticate(self) -> bool:
        """Přihlášení jako admin"""
        try:
            async with httpx.AsyncClient() as client:
                # Zkusíme různé endpointy pro přihlášení
                endpoints = [
                    f"{self.base_url}/admin/login",
                    f"{self.base_url}/auth/login",
                    f"{self.base_url}/auth/authenticate",
                    f"{self.base_url}/login"
                ]
                
                for endpoint in endpoints:
                    try:
                        print(f"🔍 Zkouším endpoint: {endpoint}")
                        response = await client.post(
                            endpoint,
                            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
                        )
                        
                        print(f"📊 Status: {response.status_code}")
                        print(f"📊 Response: {response.text[:200]}...")
                        
                        if response.status_code == 200:
                            data = response.json()
                            # Různé možnosti struktury odpovědi
                            if "data" in data and "access_token" in data["data"]:
                                self.token = data["data"]["access_token"]
                            elif "access_token" in data:
                                self.token = data["access_token"]
                            elif "token" in data:
                                self.token = data["token"]
                            else:
                                print(f"❌ Neznámá struktura odpovědi: {data}")
                                continue
                            
                            self.headers["Authorization"] = f"Bearer {self.token}"
                            print("✅ Přihlášení úspěšné!")
                            return True
                    except Exception as e:
                        print(f"❌ Chyba s endpointem {endpoint}: {e}")
                        continue
                
                print("❌ Všechny endpointy selhaly")
                return False
        except Exception as e:
            print(f"❌ Chyba připojení: {e}")
            return False
    
    async def create_collection(self, collection: str, schema: Dict[str, Any]) -> bool:
        """Vytvoření kolekce"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/collections",
                    headers=self.headers,
                    json=schema
                )
                
                if response.status_code == 200:
                    print(f"✅ Kolekce '{collection}' vytvořena")
                    return True
                else:
                    print(f"❌ Chyba při vytváření '{collection}': {response.text}")
                    return False
        except Exception as e:
            print(f"❌ Chyba: {e}")
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
                
                if response.status_code == 200:
                    print(f"✅ Pole '{field['field']}' vytvořeno v '{collection}'")
                    return True
                else:
                    print(f"❌ Chyba při vytváření pole: {response.text}")
                    return False
        except Exception as e:
            print(f"❌ Chyba: {e}")
            return False
    
    async def setup_collections(self):
        """Nastavení všech kolekcí"""
        
        # 1. Kurzy (courses)
        await self.create_collection("courses", {
            "collection": "courses",
            "meta": {
                "collection": "courses",
                "icon": "school",
                "note": "Kurzy programování",
                "display_template": "{{title}}",
                "hidden": False,
                "singleton": False,
                "translations": [
                    {
                        "language": "cs-CZ",
                        "translation": "Kurzy"
                    }
                ]
            },
            "schema": {
                "name": "courses"
            }
        })
        
        # Pole pro kurzy
        course_fields = [
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
                    "required": True,
                    "readonly": False
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
        
        for field in course_fields:
            await self.create_field("courses", field)
        
        # 2. Lekce (lessons)
        await self.create_collection("lessons", {
            "collection": "lessons",
            "meta": {
                "collection": "lessons",
                "icon": "book",
                "note": "Lekce kurzů",
                "display_template": "{{title}}",
                "hidden": False,
                "singleton": False
            },
            "schema": {
                "name": "lessons"
            }
        })
        
        # Pole pro lekce
        lesson_fields = [
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
        
        for field in lesson_fields:
            await self.create_field("lessons", field)
        
        # 3. Pokrok uživatelů (user_progress)
        await self.create_collection("user_progress", {
            "collection": "user_progress",
            "meta": {
                "collection": "user_progress",
                "icon": "trending_up",
                "note": "Pokrok uživatelů v lekcích",
                "display_template": "{{user}} - {{lesson}}",
                "hidden": False,
                "singleton": False
            },
            "schema": {
                "name": "user_progress"
            }
        })
        
        # Pole pro pokrok
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
        
        for field in progress_fields:
            await self.create_field("user_progress", field)
        
        # 4. Achievementy (achievements)
        await self.create_collection("achievements", {
            "collection": "achievements",
            "meta": {
                "collection": "achievements",
                "icon": "emoji_events",
                "note": "Odměny a úspěchy",
                "display_template": "{{name}}",
                "hidden": False,
                "singleton": False
            },
            "schema": {
                "name": "achievements"
            }
        })
        
        # Pole pro achievementy
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
        
        for field in achievement_fields:
            await self.create_field("achievements", field)
        
        # 5. Uživatelské achievementy (user_achievements)
        await self.create_collection("user_achievements", {
            "collection": "user_achievements",
            "meta": {
                "collection": "user_achievements",
                "icon": "star",
                "note": "Získané achievementy uživatelů",
                "display_template": "{{user}} - {{achievement}}",
                "hidden": False,
                "singleton": False
            },
            "schema": {
                "name": "user_achievements"
            }
        })
        
        # Pole pro uživatelské achievementy
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
        
        for field in user_achievement_fields:
            await self.create_field("user_achievements", field)
        
        print("✅ Všechny kolekce byly úspěšně vytvořeny!")
    
    async def create_sample_data(self):
        """Vytvoření ukázkových dat"""
        print("\n📝 Vytváření ukázkových dat...")
        
        # Ukázkové kurzy
        sample_courses = [
            {
                "course_id": "uvod",
                "title": "Úvod do Pythonu",
                "description": "Seznamte se se základy programování v Pythonu",
                "level": "uvod",
                "status": "published",
                "sort": 1
            },
            {
                "course_id": "zaklady",
                "title": "Základy Pythonu",
                "description": "Naučte se základní koncepty programování",
                "level": "zaklady",
                "status": "published",
                "sort": 2
            },
            {
                "course_id": "pokrocile",
                "title": "Pokročilé koncepty",
                "description": "Složitější témata pro pokročilé studenty",
                "level": "pokrocile",
                "status": "published",
                "sort": 3
            }
        ]
        
        # Vytvoření kurzů
        course_ids = {}
        for course_data in sample_courses:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.base_url}/items/courses",
                        headers=self.headers,
                        json=course_data
                    )
                    if response.status_code == 200:
                        result = response.json()
                        course_ids[course_data["course_id"]] = result["data"]["id"]
                        print(f"✅ Kurz '{course_data['title']}' vytvořen")
            except Exception as e:
                print(f"❌ Chyba při vytváření kurzu: {e}")
        
        # Ukázkové lekce
        sample_lessons = [
            # Úvod do Pythonu
            {"course": course_ids.get("uvod"), "lesson_number": 1, "title": "Co je Python?", "description": "Úvod do programování", "content": "<h1>Co je Python?</h1><p>Python je programovací jazyk...</p>", "status": "published", "sort": 1},
            {"course": course_ids.get("uvod"), "lesson_number": 2, "title": "Instalace Pythonu", "description": "Jak nainstalovat Python", "content": "<h1>Instalace Pythonu</h1><p>Stáhněte Python z python.org...</p>", "status": "published", "sort": 2},
            {"course": course_ids.get("uvod"), "lesson_number": 3, "title": "První program", "description": "Hello World!", "content": "<h1>První program</h1><p>Napište print('Hello World!')</p>", "code_example": "print('Hello World!')", "status": "published", "sort": 3},
            
            # Základy Pythonu
            {"course": course_ids.get("zaklady"), "lesson_number": 1, "title": "Proměnné", "description": "Ukládání dat", "content": "<h1>Proměnné</h1><p>Proměnná je jako krabička...</p>", "code_example": "jmeno = 'Anna'\nvěk = 15", "status": "published", "sort": 1},
            {"course": course_ids.get("zaklady"), "lesson_number": 2, "title": "Čísla a text", "description": "Datové typy", "content": "<h1>Datové typy</h1><p>Python rozlišuje čísla a text...</p>", "code_example": "cislo = 42\ntext = 'Ahoj'", "status": "published", "sort": 2},
            {"course": course_ids.get("zaklady"), "lesson_number": 3, "title": "Podmínky", "description": "if, elif, else", "content": "<h1>Podmínky</h1><p>Podmínky rozhodují o tom, co se stane...</p>", "code_example": "if věk >= 18:\n    print('Dospělý')\nelse:\n    print('Dítě')", "status": "published", "sort": 3},
            {"course": course_ids.get("zaklady"), "lesson_number": 4, "title": "Cykly", "description": "for a while", "content": "<h1>Cykly</h1><p>Cykly opakují kód...</p>", "code_example": "for i in range(5):\n    print(i)", "status": "published", "sort": 4},
            
            # Pokročilé koncepty
            {"course": course_ids.get("pokrocile"), "lesson_number": 1, "title": "Funkce", "description": "Vytváření vlastních funkcí", "content": "<h1>Funkce</h1><p>Funkce jsou bloky kódu...</p>", "code_example": "def pozdrav(jmeno):\n    return f'Ahoj, {jmeno}!'", "status": "published", "sort": 1},
            {"course": course_ids.get("pokrocile"), "lesson_number": 2, "title": "Seznamy", "description": "Práce s daty", "content": "<h1>Seznamy</h1><p>Seznamy ukládají více hodnot...</p>", "code_example": "barvy = ['červená', 'modrá', 'zelená']", "status": "published", "sort": 2},
            {"course": course_ids.get("pokrocile"), "lesson_number": 3, "title": "Soubory", "description": "Čtení a zápis do souborů", "content": "<h1>Soubory</h1><p>Python umí číst a zapisovat soubory...</p>", "code_example": "with open('soubor.txt', 'r') as f:\n    obsah = f.read()", "status": "published", "sort": 3}
        ]
        
        # Vytvoření lekcí
        for lesson_data in sample_lessons:
            if lesson_data["course"]:  # Pouze pokud existuje kurz
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            f"{self.base_url}/items/lessons",
                            headers=self.headers,
                            json=lesson_data
                        )
                        if response.status_code == 200:
                            print(f"✅ Lekce '{lesson_data['title']}' vytvořena")
                except Exception as e:
                    print(f"❌ Chyba při vytváření lekce: {e}")
        
        # Ukázkové achievementy
        sample_achievements = [
            {
                "name": "První kroky",
                "description": "Dokončil jste první lekci",
                "icon": "fas fa-play",
                "points": 10,
                "condition_type": "lessons_completed",
                "condition_value": 1,
                "status": "published"
            },
            {
                "name": "Programátor",
                "description": "Spustil jste kód v Playground",
                "icon": "fas fa-code",
                "points": 20,
                "condition_type": "lessons_completed",
                "condition_value": 3,
                "status": "published"
            },
            {
                "name": "Výdrž",
                "description": "Učte se 7 dní v řadě",
                "icon": "fas fa-fire",
                "points": 50,
                "condition_type": "time_spent",
                "condition_value": 7,
                "status": "published"
            },
            {
                "name": "Absolvent",
                "description": "Dokončete všechny kurzy",
                "icon": "fas fa-graduation-cap",
                "points": 100,
                "condition_type": "lessons_completed",
                "condition_value": 10,
                "status": "published"
            }
        ]
        
        # Vytvoření achievementů
        for achievement_data in sample_achievements:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.base_url}/items/achievements",
                        headers=self.headers,
                        json=achievement_data
                    )
                    if response.status_code == 200:
                        print(f"✅ Achievement '{achievement_data['name']}' vytvořen")
            except Exception as e:
                print(f"❌ Chyba při vytváření achievementu: {e}")
        
        print("✅ Ukázková data byla úspěšně vytvořena!")

async def main():
    """Hlavní funkce"""
    print("🚀 Directus Setup pro Python Kurz")
    print("=" * 50)
    
    setup = DirectusSetup()
    
    # Přihlášení
    if not await setup.authenticate():
        print("❌ Nelze se přihlásit do Directus. Zkontrolujte údaje.")
        return
    
    # Vytvoření kolekcí
    print("\n📚 Vytváření kolekcí...")
    await setup.setup_collections()
    
    # Vytvoření ukázkových dat
    await setup.create_sample_data()
    
    print("\n🎉 Setup dokončen!")
    print("\n📋 Další kroky:")
    print("1. Zkontrolujte kolekce v Directus admin panelu")
    print("2. Nastavte oprávnění pro Public a Authenticated role")
    print("3. Vytvořte Directus token pro API")
    print("4. Aktualizujte .env soubor s tokenem")

if __name__ == "__main__":
    asyncio.run(main())
