import pytest
from app.database import async_session
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_async_session_direct():
    async with async_session() as session:
        assert isinstance(session, AsyncSession)
        print(f"[DEBUG] AsyncSession instance: {session}")
