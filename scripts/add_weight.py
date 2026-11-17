#!/usr/bin/env python3
import json
import os
import sys
from datetime import date

# Путь к файлу weight.json (в папке уровнем выше scripts/)
JSON_FILE = os.path.join(os.path.dirname(__file__), '..', 'weight.json')

def add_weight(weight, note=''):
    # Загружаем существующие данные (если файл есть)
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # Если файла нет — создаём полную структуру
        data = {
            "weight_journal": {
                "version": "1.0",
                "created": date.today().isoformat(),
                "updated": date.today().isoformat(),
                "author": "Евгений Миронов (EvgenMironov900)",
                "entries": []
            }
        }
    
    # Добавляем запись
    data["weight_journal"]["entries"].append({
        "date": date.today().isoformat(),
        "weight": weight,
        "note": note
    })
    
    # Обновляем дату (если поле есть)
    if "updated" in data["weight_journal"]:
        data["weight_journal"]["updated"] = date.today().isoformat()
    
    # Сохраняем
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    
    print(f"✅ Добавлено: {date.today().isoformat()} — {weight} кг")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: python3 add_weight.py <вес> [комментарий]")
        sys.exit(1)
    
    try:
        weight = float(sys.argv[1])
    except ValueError:
        print("❌ Вес должен быть числом")
        sys.exit(1)
    
    note = sys.argv[2] if len(sys.argv) > 2 else ''
    add_weight(weight, note)
