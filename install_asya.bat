@echo off
setlocal
title ASYA Installer

echo ===================================================
echo   ASYA: Автоматическая установка (Windows)
echo ===================================================
echo.

:: 1. Проверка Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден!
    echo Пожалуйста, установите Python с сайта https://www.python.org/
    echo При установке обязательно поставьте галочку "Add Python to PATH".
    pause
    exit /b
)

:: 2. Проверка Node.js
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Node.js не найден!
    echo Пожалуйста, установите Node.js с сайта https://nodejs.org/
    pause
    exit /b
)

:: 3. Запуск основного скрипта настройки
echo [OK] Зависимости найдены. Запуск настройки...
echo.
python asya_auto_setup.py

if %errorlevel% neq 0 (
    echo.
    echo [ОШИБКА] Произошла ошибка во время установки.
) else (
    echo.
    echo [ГОТОВО] Установка АСИ завершена успешно!
)

pause
