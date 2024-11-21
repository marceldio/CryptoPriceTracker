import asyncio
from app.database import async_session, save_price_to_db

async def add_test_data():
    test_data = [
        {"ticker": "btc_usd", "price": 50550, "timestamp": 1711975140},
        {"ticker": "btc_usd", "price": 51050, "timestamp": 1731975140},
    ]
    async with async_session() as session:
        for data in test_data:
            await save_price_to_db(session, data)

asyncio.run(add_test_data())
