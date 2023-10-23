import os
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(
    os.getenv("POSTGRES_URL"),
    future=True,
    echo=False,
    execution_options={"isolation_level": "AUTOCOMMIT"},
    pool_use_lifo=True,
    pool_pre_ping=True,
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
