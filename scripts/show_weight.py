#!/usr/bin/env python3

# Версия от 15 ноября 2026г.
# Добавлен пропуск средних записей weight.json и согласование падежа количечества пропущенных строк
import json
import os
from Прибамбасы import Соглпад

# Путь к файлу weight.json (в папке уровнем выше scripts/)
JSON_FILE = os.path.join(os.path.dirname(__file__), '..', 'weight.json')

# Сколько первых и последних записей показывать при сворачивании
HEAD_COUNT = 2
TAIL_COUNT = 3
COLLAPSE_THRESHOLD = HEAD_COUNT + TAIL_COUNT + 2  # 7: при 8+ сворачиваем

def format_entry(entry):
    note = entry.get('note', '')
    if note:
        return f"{entry['date']} — {entry['weight']} кг — {note}"
    return f"{entry['date']} — {entry['weight']} кг"

def show_weight():
    if not os.path.exists(JSON_FILE):
        print("❌ Файл weight.json не найден.")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if "weight_journal" not in data or "entries" not in data["weight_journal"]:
        print("❌ Ошибка: неверная структура JSON.")
        return

    entries = data["weight_journal"]["entries"]

    if not entries:
        print("📊 Нет записей.")
        return

    print("📊 Динамика веса:")
    print("-" * 40)

    if len(entries) <= COLLAPSE_THRESHOLD:
        # Показываем всё
        for entry in entries:
            print(format_entry(entry))
    else:
        # Сворачиваем: первые HEAD_COUNT, многоточие, последние TAIL_COUNT
        for entry in entries[:HEAD_COUNT]:
            print(format_entry(entry))
        
        skipped = len(entries) - HEAD_COUNT - TAIL_COUNT
        print(f"... (пропущено {skipped} {Соглпад(skipped, ('записей', 'запись', 'записи'))}) ...")        
        
        
        for entry in entries[-TAIL_COUNT:]:
            print(format_entry(entry))

    # Расчёт изменения (если есть хотя бы 2 записи)
    # if len(entries) >= 2:
    #     first = entries[0]['weight']
    #     last = entries[-1]['weight']
    #     diff = last - first
    #     print("-" * 40)
    #     print(f"📉 Изменение: {diff:+.2f} кг")
    if len(entries) >= 2:
        first = entries[0]['weight']
        last = entries[-1]['weight']
        diff = last - first
        print("-" * 40)
        print(f"📉 Изменение: {diff:+.3f} кг")

        # Скорость изменения: честное количество дней, округление до 10 г
        from datetime import date
        d_first = date.fromisoformat(entries[0]['date'])
        d_last = date.fromisoformat(entries[-1]['date'])
        days = (d_last - d_first).days
        if days > 0:
            speed_g = diff * 1000 / days          # граммы в день
            speed_10 = round(speed_g / 10) * 10   # округление до 10 г
            print(f"⚖️ Скорость изменения: {speed_10:+.0f} г/день")


if __name__ == '__main__':
    show_weight()
