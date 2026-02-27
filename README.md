# Qwen (GGUF) server for Railway via llama.cpp

Это отдельный сервис **Qwen API** (OpenAI-compatible), который бот будет дергать по внутреннему адресу Railway.

## 1) Создай новый сервис в Railway
- New Service → **GitHub Repository** → выбери этот репозиторий.

## 2) Подключи Volume
- Attach Volume
- Mount Path: `/data`

## 3) Залей модель в Volume
- Переименуй файл модели в `Qwen.gguf` (чтобы проще).
- Внутри volume файл должен лежать как: `/data/Qwen.gguf`

## 4) Variables (в сервисе Qwen)
- `MODEL_PATH=/data/Qwen.gguf`
- `PORT=8081`

## 5) Проверка
После Deploy у сервиса должны появиться логи про запуск сервера.
Внутри Railway сетью он будет доступен по:
- `http://<service-name>:8081`

(если сервис назван `llamacpp`, то `http://llamacpp:8081`)

Эндпоинты:
- `GET /v1/models`
- `POST /v1/chat/completions`

## 6) В сервисе бота
В Variables бота поставь:
- `QWEN_BASE_URL=http://<service-name>:8081`

Пример:
- `QWEN_BASE_URL=http://llamacpp:8081`
