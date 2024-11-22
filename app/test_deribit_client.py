import asyncio
import aiohttp
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.deribit_client import DeribitClient
from app.database import DATABASE_URL
from app.database import save_price_to_db


# Создаем асинхронный движок и сессию
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine)


async def main():
    async with aiohttp.ClientSession() as session:
        async with async_session() as db_session:
            client = DeribitClient(session, db_session)
            # Добавляем проверку вызова save_price_to_db
            for ticker in ["btc_usd", "eth_usd"]:
                price_data = await client.fetch_price(ticker)
                print(f"Attempting to save data for {ticker}: {price_data}")  # Отладочный вывод
                await save_price_to_db(db_session, price_data)

if __name__ == "__main__":
    asyncio.run(main())
