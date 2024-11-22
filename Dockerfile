# Указываем базовый образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Копируем исходный код приложения
COPY . /app/

# Копируем файл переменных окружения для Docker
COPY .env.docker /app/.env

# Указываем команду для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
