from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session
from app.models import Price
from sqlalchemy import select, and_, desc, bindparam
from typing import AsyncGenerator
from dotenv import load_dotenv
import os
from app.deribit_client import DeribitClient
import aiohttp
import asyncio
from contextlib import asynccontextmanager


# Загружаем переменные окружения из .env файла
load_dotenv()

# Используем переменные
DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG = os.getenv("DEBUG", "False") == "True"
SECRET_KEY = os.getenv("SECRET_KEY")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with aiohttp.ClientSession() as session:
        client = DeribitClient(session=session, db_session=async_session())
        asyncio.create_task(client.run())
        yield  # Логика продолжится после старта приложения


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Welcome to CryptoPriceTracker API"}


# Функция для получения сессии
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@app.get("/prices/")
async def get_prices(
    ticker: str = Query(..., description="Ticker of the currency (e.g., btc_usd, eth_usd)"),
    session: AsyncSession = Depends(get_session),
):
    stmt = (
        select(Price)
        .where(
            and_(
                Price.ticker == bindparam('ticker'),
                Price.timestamp > 0
            )
        )
    )
    params = {'ticker': ticker}
    result = await session.execute(stmt, params)
    prices = result.scalars().all()
    if not prices:
        raise HTTPException(status_code=404, detail="No data found")
    return prices


@app.get("/prices/last/")
async def get_last_price(
    ticker: str = Query(..., description="Ticker of the currency (e.g., btc_usd, eth_usd)"),
    session: AsyncSession = Depends(get_session),
):
    # noinspection PyTypeChecker
    stmt = (
        select(Price)
        .where(Price.ticker == bindparam('ticker'))
        .order_by(desc(Price.timestamp))
        .limit(1)
    )

    params = {'ticker': ticker}
    result = await session.execute(stmt, params)
    price = result.scalar_one_or_none()
    if not price:
        raise HTTPException(status_code=404, detail="No data found")
    return price


@app.get("/prices/filter/")
async def get_filtered_prices(
    ticker: str = Query(..., description="Ticker of the currency (e.g., btc_usd, eth_usd)"),
    start_date: int = Query(..., description="Start date as UNIX timestamp"),
    end_date: int = Query(..., description="End date as UNIX timestamp"),
    session: AsyncSession = Depends(get_session),
):
    stmt = (
        select(Price)
        .where(
            and_(
                Price.ticker == bindparam('ticker'),
                Price.timestamp.between(bindparam('start_date'), bindparam('end_date'))
            )
        )
    )
    params = {'ticker': ticker, 'start_date': start_date, 'end_date': end_date}
    result = await session.execute(stmt, params)
    prices = result.scalars().all()
    if not prices:
        raise HTTPException(status_code=404, detail="No data found")
    return prices
