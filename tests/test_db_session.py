# import pytest
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.sql import text
#
# @pytest.mark.asyncio
# async def test_db_session_fixture(db_session):
#     # Убедитесь, что db_session возвращает объект AsyncSession
#     assert db_session is not None
#     assert isinstance(db_session, AsyncSession)
#
#     # Проверяем вставку и выборку данных
#     await db_session.execute(
#         text("INSERT INTO prices (ticker, price, timestamp) VALUES ('btc_usd', 50000, 1700000000)")
#     )
#     await db_session.commit()
#
#     result = await db_session.execute(text("SELECT * FROM prices"))
#     rows = [dict(row) for row in result]
#     print("Rows in prices:", rows)
#
#     assert len(rows) == 1
#     assert rows[0]["ticker"] == "btc_usd"
#     assert rows[0]["price"] == 50000
#     assert rows[0]["timestamp"] == 1700000000
