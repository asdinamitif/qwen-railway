import os
import subprocess
import sys
import json

def run_command(command, description):
    print(f"--- {description} ---")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении: {e}")
        return False
    return True

def main():
    print("=== ASYA: Автоматическая настройка рабочего окружения ===")

    # 1. Проверка Node.js
    if not run_command("node -v", "Проверка Node.js"):
        print("Node.js не найден. Пожалуйста, установите Node.js 24+ с сайта nodejs.org")
        return

    # 2. Установка Ruflo
    if run_command("npx ruflo@latest init --non-interactive", "Установка Ruflo"):
        print("Ruflo успешно инициализирован.")

    # 3. Добавление Shannon
    run_command("npx skills add unicodeveloper/shannon", "Интеграция Shannon")

    # 4. Установка agent-browser
    if run_command("npm install -g agent-browser", "Установка agent-browser"):
        run_command("agent-browser install --with-deps", "Настройка браузера для агентов")

    # 5. Настройка подключения к бэкенду
    railway_url = input("\nВведите URL вашего бэкенда на Railway (например, https://asya-brain.up.railway.app): ")

    config = {
        "asya_backend_url": railway_url,
        "persona": "ASYA",
        "version": "1.0.0"
    }

    with open("asya_config.json", "w") as f:
        json.dump(config, f, indent=4)

    print("\n=== Настройка завершена! ===")
    print(f"1. Ваш бэкенд: {railway_url}")
    print("2. Теперь откройте OpenHuman и добавьте MCP сервер Ruflo:")
    print("   Команда: npx ruflo@latest mcp start")
    print("3. Скопируйте системный промт из файла asya_system_prompt.txt в настройки OpenHuman.")

if __name__ == "__main__":
    main()
