# 🐳 Dockerfile — окружение для запуска автотестов

FROM python:3.10-slim

# Установка переменных среды
ENV POETRY_VIRTUALENVS_IN_PROJECT=1 \
    PYTHONWARNINGS="ignore:Unverified HTTPS request" \
    PIP_DEFAULT_TIMEOUT=60 \
    POETRY_REQUESTS_TIMEOUT=60

# Создание рабочей директории
WORKDIR /tmp/aft_tests

# Установка Poetry и настройка доступа к приватному репозиторию
ARG TOKEN
RUN pip install --no-cache-dir --upgrade \
    && pip install \
        --extra-index-url https://TOKEN@sberosci.sigma.sbrf.ru/repo/pypi/simple \
        poetry==1.8.3

COPY poetry.lock pyproject.toml ./

RUN poetry config http-basic.pypi-sigma token "$TOKEN" \
    && poetry config certificates.pypi-sigma.cert false \
    && poetry install -vvv --no-root --no-cache --no-interaction

# Копируем проект
COPY . .

# Права и точка входа
RUN chmod -R 777 /tmp/aft_tests/test_data reports \
    && chmod +x entrypoint.sh

# Запуск скрипта
ENTRYPOINT ["./entrypoint.sh"]