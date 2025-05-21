FROM python:3.11-slim

WORKDIR /app

# 🧱 Установка системных библиотек для работы headless Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libxcursor1 \
    libxrandr2 \
    libxcomposite1 \
    libasound2 \
    libxdamage1 \
    libx11-xcb1 \
    libgtk-3-0 \
    libgbm1 \
    fonts-liberation \
    libu2f-udev \
    libvulkan1 \
 && apt-get clean

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["pytest", "tests/", "--alluredir=allure-results"]
