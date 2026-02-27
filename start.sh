#!/usr/bin/env bash
set -e

echo "=== Checking model in /data ==="

if [ ! -f /data/Qwen.gguf ]; then
  echo "Downloading model..."
  curl -L --fail --retry 3 -o /data/Qwen.gguf "$MODEL_URL"
fi

echo "=== Starting Qwen server on 8081 ==="
/opt/llama.cpp/build/bin/llama-server \
  -m /data/Qwen.gguf \
  --host 0.0.0.0 \
  --port 8081 \
  -t 24 \
  -c 4096 &

sleep 5

echo "=== Starting bot ==="
python3 bot.py
