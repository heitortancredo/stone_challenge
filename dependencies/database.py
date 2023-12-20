from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.postgressql import session_maker

async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session