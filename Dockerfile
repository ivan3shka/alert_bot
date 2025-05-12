FROM python:3.11-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    xvfb \
    ca-certificates \
    libappindicator1 \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libgbm1 \
    libgtk-3-0 \
    libpangocairo-1.0-0 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Установка Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование кода
COPY . .

# Установка Python зависимостей
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Запуск xvfb перед запуском скрипта
CMD ["sh", "-c", "Xvfb :99 -ac & python3 main.py"]
