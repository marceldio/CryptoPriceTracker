import pytest
from app.database import async_session


@pytest.mark.asyncio
async def test_async_session_direct():
    async with async_session() as session:
        assert session is not None
