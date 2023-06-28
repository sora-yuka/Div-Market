from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from decouple import config


class Base(DeclarativeBase):
    pass



engine = create_async_engine(f"postgresql+asyncpg://{config('DATABASE_URL')}")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session