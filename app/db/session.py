from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from collections.abc import AsyncGenerator
import logging

logger = logging.getLogger(__name__)

# To be replaced later with a call to an environment file
username = "devrelay_user"
password = "devrelay_pass"
host = "localhost"
db_name = "devrelay_db"
database_url = f"postgresql+asyncpg://{username}:{password}@{host}/{db_name}"
engine = create_async_engine(database_url)
async_session = async_sessionmaker(engine)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:

    async with async_session() as session:
        try:
            await session.begin()
            yield session
            await session.commit()
        # we do not know the nature of the exceptions that could be raised at this layer
        except Exception:
            await session.rollback()
            logger.exception("Database session error")
            raise