import pytest
from tests.conftest import db_session
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_conftest_db_session(db_session):
    print(f"[DEBUG] Fixture db_session in test_conftest: {db_session}")
    assert db_session is not None
    assert isinstance(db_session, AsyncSession)
