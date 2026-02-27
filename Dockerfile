# Qwen (GGUF) OpenAI-compatible server via llama.cpp (llama-server)
# Deploy as a separate Railway service with a Volume mounted to /data
# Put your model file as /data/Qwen.gguf

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates git build-essential cmake curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone --depth 1 https://github.com/ggerganov/llama.cpp.git

WORKDIR /opt/llama.cpp
# Build llama-server
RUN cmake -S . -B build -DLLAMA_BUILD_SERVER=ON -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DCMAKE_BUILD_TYPE=Release \
 && cmake --build build -j

EXPOSE 8081

# You can override MODEL_PATH / PORT via Railway Variables
ENV MODEL_PATH=/data/Qwen.gguf
ENV PORT=8081

CMD ["/bin/bash","-lc","./build/bin/llama-server -m ${MODEL_PATH} --host 0.0.0.0 --port ${PORT}"]
