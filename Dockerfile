FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Команда по умолчанию (может быть пустой, т.к. Jenkins будет запускать команды)
CMD ["pytest"]
