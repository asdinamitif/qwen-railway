FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git build-essential cmake curl ca-certificates python3 python3-pip \
 && rm -rf /var/lib/apt/lists/*

# ---------- Установка llama.cpp ----------
RUN git clone https://github.com/ggerganov/llama.cpp /opt/llama.cpp
WORKDIR /opt/llama.cpp
RUN cmake -B build && cmake --build build -j

# ---------- Копируем проект ----------
WORKDIR /app
COPY . /app

# зависимости бота
RUN if [ -f requirements.txt ]; then pip3 install --no-cache-dir -r requirements.txt; fi

# запуск
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]
