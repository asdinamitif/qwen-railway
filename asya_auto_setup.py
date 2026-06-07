import os
import subprocess
import sys
import json
import time

def run_command(command, description):
    print(f"\n--- {description} ---")
    print(f"Выполняю: {command}")
    try:
        # Для Windows npm команд используем shell=True
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Ошибка при выполнении: {e}")
        return False
    return True

def main():
    print("\n" + "="*50)
    print("      АСЯ: МАСТЕР АВТОМАТИЧЕСКОЙ НАСТРОЙКИ")
    print("="*50)
    print("\nЭтот скрипт настроит всё необходимое для работы вашей помощницы.")

    # 1. Проверка Node.js и Python зависимостей
    print("\n[1/6] Проверка окружения...")
    run_command("pip install customtkinter requests openai pyttsx3 SpeechRecognition", "Установка Python библиотек для GUI")

    if not run_command("node -v", "Версия Node.js"):
        print("ОШИБКА: Node.js не найден. Установите его с nodejs.org")
        sys.exit(1)

    # 2. Установка Ruflo
    print("\n[2/5] Настройка Ruflo (Нервная система)...")
    run_command("npm install -g ruflo@latest", "Глобальная установка Ruflo")
    run_command("npx ruflo@latest init --non-interactive", "Инициализация Ruflo")

    # 3. Добавление Shannon
    print("\n[3/5] Интеграция Shannon (Безопасность)...")
    run_command("npx skills add unicodeveloper/shannon", "Добавление навыка Shannon")

    # 4. Установка agent-browser
    print("\n[4/6] Настройка браузерной автоматизации...")
    if run_command("npm install -g agent-browser", "Установка Vercel agent-browser"):
        print("Скачивание необходимых компонентов браузера (это может занять время)...")
        run_command("agent-browser install --with-deps", "Загрузка Chromium")

    # 5. Установка Deskreen и Flow Launcher (только для Windows)
    if os.name == 'nt':
        print("\n[5/6] Установка дополнительных инструментов (Windows)...")
        run_command("winget install Flow-Launcher.Flow-Launcher --silent", "Установка Flow Launcher")
        run_command("winget install pavlobu.deskreen --silent", "Установка Deskreen")

    # 6. Настройка бэкенда
    print("\n[6/6] Финальная конфигурация...")
    print("\nШаг 1: Разверните бэкенд на Railway (если еще не сделали этого).")
    print("Шаг 2: Скопируйте URL вашего развернутого сервиса.")

    railway_url = input("\nВведите URL вашего бэкенда (например, https://asya.up.railway.app): ").strip()
    if not railway_url:
        railway_url = "http://localhost:8081" # Fallback

    if not railway_url.endswith("/v1"):
        if railway_url.endswith("/"):
            railway_url += "v1"
        else:
            railway_url += "/v1"

    config = {
        "asya_backend_url": railway_url,
        "persona": "ASYA",
        "timestamp": time.ctime()
    }

    with open("asya_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    print("\n" + "="*50)
    print("           УСТАНОВКА ЗАВЕРШЕНА!")
    print("="*50)
    print(f"\n1. Ваш бэкенд настроен: {railway_url}")
    print("2. ТЕПЕРЬ САМОЕ ВАЖНОЕ:")
    print("   - Откройте приложение OpenHuman.")
    print("   - В настройках (Settings -> MCP) добавьте:")
    print("     Command: npx")
    print("     Args: ruflo@latest mcp start")
    print("   - В настройках модели укажите ваш URL бэкенда.")
    print("\nТеперь вы можете просто сказать: 'АСЯ, привет!'")
    print("="*50 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nУстановка прервана пользователем.")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
