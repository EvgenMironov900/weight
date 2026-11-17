#!/usr/bin/env python3
import json
import os
from datetime import date

JSON_FILE = os.path.join(os.path.dirname(__file__), '..', 'weight.json')

def migrate():
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    if not isinstance(old_data, list):
        print("❌ Файл уже мигрирован (не массив)")
        return
    
    new_data = {
        "weight_journal": {
            "version": "1.0",
            "created": date.today().isoformat(),
            "updated": date.today().isoformat(),
            "author": "Евгений Миронов (EvgenMironov900)",
            "entries": old_data
        }
    }
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    
    print(f"✅ Миграция завершена. Записей: {len(old_data)}")

if __name__ == '__main__':
    migrate()
