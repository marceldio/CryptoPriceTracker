from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.models import Base, Price


DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_price_to_db(session: AsyncSession, price_data: dict):
    price = Price(**price_data)
    session.add(price)
    await session.commit()
