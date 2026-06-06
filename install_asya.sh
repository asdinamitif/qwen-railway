#!/usr/bin/env bash

echo "==================================================="
echo "  ASYA: Автоматическая установка (macOS/Linux)"
echo "==================================================="
echo

# 1. Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "[ОШИБКА] Python 3 не найден!"
    echo "Пожалуйста, установите Python 3: brew install python (macOS) или apt install python3 (Linux)"
    exit 1
fi

# 2. Проверка Node.js
if ! command -v node &> /dev/null; then
    echo "[ОШИБКА] Node.js не найден!"
    echo "Пожалуйста, установите Node.js 24+ с сайта https://nodejs.org/"
    exit 1
fi

# 3. Запуск основного скрипта настройки
echo "[OK] Зависимости найдены. Запуск настройки..."
echo
python3 asya_auto_setup.py

if [ $? -ne 0 ]; then
    echo
    echo "[ОШИБКА] Произошла ошибка во время установки."
else
    echo
    echo "[ГОТОВО] Установка АСИ завершена успешно!"
fi
