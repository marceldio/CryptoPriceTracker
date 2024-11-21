import asyncio
from app.database import async_session, save_price_to_db

# Тестовые данные для записи
test_data = {
    "ticker": "btc_usd",
    "price": 50000.0,
    "timestamp": 1700000000,  # Пример UNIX-времени
}

async def test_insert():
    async with async_session() as session:
        # Вставляем тестовые данные
        await save_price_to_db(session, test_data)
        print("Test data inserted successfully!")

# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_insert())
