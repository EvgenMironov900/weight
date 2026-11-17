#!/usr/bin/env python3
import json
import os
import sys

# Путь к файлу weight.json (в папке уровнем выше scripts/)
JSON_FILE = os.path.join(os.path.dirname(__file__), '..', 'weight.json')

def remove_weight(date_to_remove):
    # Проверяем, что файл существует
    if not os.path.exists(JSON_FILE):
        print("❌ Файл weight.json не найден.")
        return
    
    # Загружаем данные
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Проверяем структуру
    if "weight_journal" not in data or "entries" not in data["weight_journal"]:
        print("❌ Ошибка: неверная структура JSON.")
        return
    
    entries = data["weight_journal"]["entries"]
    
    # Ищем запись с указанной датой
    initial_length = len(entries)
    entries = [entry for entry in entries if entry["date"] != date_to_remove]
    
    if len(entries) == initial_length:
        print(f"⚠️ Запись с датой {date_to_remove} не найдена.")
        return
    
    # Обновляем данные
    data["weight_journal"]["entries"] = entries
    
    # Обновляем дату (если поле есть)
    if "updated" in data["weight_journal"]:
        from datetime import date
        data["weight_journal"]["updated"] = date.today().isoformat()
    
    # Сохраняем
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    
    print(f"✅ Удалена запись с датой: {date_to_remove}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: python3 remove_weight.py <дата в формате YYYY-MM-DD>")
        sys.exit(1)
    
    remove_weight(sys.argv[1])
