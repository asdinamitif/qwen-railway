#!/usr/bin/env bash
set -e

echo "=== Checking model in /data ==="

if [ ! -f /data/Qwen.gguf ]; then
  echo "Downloading model..."
  curl -L --fail --retry 3 -o /data/Qwen.gguf "${MODEL_URL:-https://huggingface.co/HauhauCS/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive/resolve/main/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q6_K.gguf?download=true}"
fi

if [ ! -f /data/mmproj.gguf ]; then
  echo "Downloading vision encoder..."
  curl -L --fail --retry 3 -o /data/mmproj.gguf "${MMPROJ_URL:-https://huggingface.co/HauhauCS/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive/resolve/main/mmproj-Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-BF16.gguf?download=true}"
fi

echo "=== Starting ASYA (Qwen server) ==="

/opt/llama.cpp/build/bin/llama-server \
  -m /data/Qwen.gguf \
  --mmproj /data/mmproj.gguf \
  --host 0.0.0.0 \
  --port 8081 \
  -t 24 \
  -c 4096
