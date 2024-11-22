import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"


@pytest.mark.asyncio(loop_scope="function")
async def test_get_prices(client, db_session: AsyncSession):
    """Тест для проверки получения списка цен."""
    # Добавление данных в базу
    await db_session.execute(
        text(
            "INSERT INTO prices (ticker, price, timestamp) VALUES "
            "('btc_usd', 50000, 1700000000)"
        )
    )
    await db_session.commit()

    # Запрос к API
    response = await client.get("/prices/?ticker=btc_usd")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["ticker"] == "btc_usd"


@pytest.mark.asyncio(loop_scope="function")
async def test_get_last_price(client, db_session: AsyncSession):
    """Тест для проверки получения последней цены."""
    await db_session.execute(
        text(
            "INSERT INTO prices (ticker, price, timestamp) VALUES "
            "('btc_usd', 50000, 1700000000)"
        )
    )
    await db_session.commit()

    response = await client.get("/prices/last/?ticker=btc_usd")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "btc_usd"


@pytest.mark.asyncio(loop_scope="function")
async def test_get_filtered_prices(client, db_session: AsyncSession):
    """Тест для проверки фильтрации цен."""
    await db_session.execute(
        text(
            "INSERT INTO prices (ticker, price, timestamp) VALUES "
            "('btc_usd', 50000, 1700000000),"
            "('btc_usd', 50500, 1700001000),"
            "('btc_usd', 51000, 1700002000)"
        )
    )
    await db_session.commit()

    # Устанавливаем фильтр по времени
    response = await client.get(
        "/prices/filter/?ticker=btc_usd&start_date=1700000000"
        "&end_date=1700001999"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Должно вернуться 2 записи
    assert data[0]["price"] == 50000
    assert data[1]["price"] == 50500
