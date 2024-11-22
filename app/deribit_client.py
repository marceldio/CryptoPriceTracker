import aiohttp
from datetime import datetime, timezone
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import save_price_to_db

BASE_URL = "https://www.deribit.com/api/v2/public/get_index_price"

class DeribitClient:
    def __init__(self, session: aiohttp.ClientSession, db_session: AsyncSession):
        self.session = session
        self.db_session = db_session

    async def fetch_price(self, ticker: str) -> dict:
        params = {"index_name": ticker}
        async with self.session.get(BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                print(f"Fetched data for {ticker}: {data}")  # Добавлено логирование
                current_time = datetime.now(timezone.utc)
                return {
                    "ticker": ticker,
                    "price": data["result"]["index_price"],
                    "timestamp": int(current_time.timestamp())
                }
            else:
                print(f"Failed to fetch {ticker}, status: {response.status}")  # Логирование ошибок
                raise Exception(f"Failed to fetch {ticker}, status: {response.status}")


    async def run(self):
        while True:
            for ticker in ["btc_usd", "eth_usd"]:
                try:
                    price_data = await self.fetch_price(ticker)
                    await save_price_to_db(self.db_session, price_data)
                except Exception as e:
                    print(f"Error fetching data: {e}")
            await asyncio.sleep(60)
