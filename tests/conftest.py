import pytest_asyncio
from app.database import async_session, init_db
from app.main import app
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
import asyncio


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Создание одного цикла событий на сессию."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Настраиваем базу данных перед каждым тестом
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    """Фикстура для создания таблиц в базе данных перед тестами."""
    await init_db()  # Создаем таблицы в базе данных
    yield
    # Очищаем данные после тестов (опционально)
    async with async_session() as session:
        await session.execute(text("TRUNCATE TABLE prices RESTART IDENTITY CASCADE;"))
        await session.commit()


# Сессия базы данных для тестов
@pytest_asyncio.fixture
async def db_session():
    """Фикстура для предоставления асинхронной сессии базы данных."""
    async with async_session() as session:
        yield session
        await session.rollback()  # Откат изменений после каждого теста


# HTTP-клиент для тестов
@pytest_asyncio.fixture
async def client(db_session):
    """Фикстура для HTTP-клиента."""
    # Убедимся, что app использует изолированный контекст
    app.dependency_overrides = {}  # Очистка зависимостей
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as c:
        yield c
