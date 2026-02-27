FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git cmake build-essential wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone https://github.com/ggerganov/llama.cpp && \
    cd llama.cpp && cmake -S . -B build && cmake --build build -j

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
