# import pytest
# from sqlalchemy.ext.asyncio import AsyncSession
#
#
# @pytest.mark.asyncio
# async def test_db_session_fixture_basic(db_session):
#     print(f"[DEBUG] Test received db_session: {db_session}")
#     assert db_session is not None
#     assert isinstance(db_session, AsyncSession)
#     await db_session.execute("SELECT 1")  # Проверка запроса
