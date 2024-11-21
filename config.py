import os

# Основной URL базы данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Тестовый URL базы данных
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")

# Если тесты запускаются, используем тестовую базу данных
if os.getenv("PYTEST_RUNNING", "0") == "1":
    DATABASE_URL = DATABASE_URL_TEST


# Если переменные окружения не заданы, выбрасываем исключение
if not DATABASE_URL:
    raise ValueError("DATABASE_URL не задан. Проверьте переменные окружения.")
