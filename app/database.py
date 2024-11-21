from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os
from app.models import Base


# Загрузка переменных окружения
load_dotenv()

# Переменные окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем асинхронный sessionmaker
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    print("Models in Base.metadata:", Base.metadata.tables.keys())  # Отладка
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_price_to_db(session: AsyncSession, price_data: dict):
    from app.models import Price  # Импорт модели здесь, чтобы избежать циклического импорта
    price = Price(**price_data)
    session.add(price)
    await session.commit()
