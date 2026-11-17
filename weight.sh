#!/bin/bash

# Определяем папку, где лежит этот скрипт (чтобы работало из любого места)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Проверка: если передан аргумент — добавляем вес, иначе показываем
if [ -n "$1" ]; then
    # Добавляем вес (аргумент 1) и, если есть, комментарий (аргумент 2)
    if [ -n "$2" ]; then
        "$SCRIPT_DIR/scripts/add_weight.py" "$1" "$2"
    else
        "$SCRIPT_DIR/scripts/add_weight.py" "$1"
    fi
fi
# Показываем динамику
"$SCRIPT_DIR/scripts/show_weight.py"

