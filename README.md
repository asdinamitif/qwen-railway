# ASYA Assistant (Backend)
# Qwen (GGUF) server for Railway via llama.cpp

> **[СКАЧАТЬ ПРИЛОЖЕНИЕ (Desktop App)](https://github.com/tinyhumansai/openhuman/releases/latest)** — установите это на свой компьютер, чтобы запустить АСЮ.


This is a standalone **Qwen API** server (OpenAI-compatible) designed for deployment on Railway using `llama.cpp`. It allows you to run Qwen language models locally (in GGUF format) and access them via a standard API.

## Project Architecture
- **Engine**: [llama.cpp](https://github.com/ggerganov/llama.cpp) (compiled from source during Docker build).
- **Model**: Qwen (GGUF format), downloaded automatically on first run.
- **Deployment**: Optimized for Railway with Volume support for persistent model storage.
- **API**: OpenAI-compatible (supports `/v1/chat/completions`).

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
