@echo off
setlocal
title ASYA Runner

echo ===================================================
echo   ASYA: Запуск ассистента
echo ===================================================
echo.

if not exist asya_config.json (
    echo [!] ОШИБКА: Файл конфигурации не найден.
    echo Пожалуйста, сначала запустите install_asya.bat для настройки.
    pause
    exit /b
)

echo [OK] Запуск графического интерфейса...
python asya_gui.py

if %errorlevel% neq 0 (
    echo.
    echo [!] Произошла ошибка при запуске. Убедитесь, что Python установлен.
    pause
)
