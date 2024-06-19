from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings
from database.models import ValuesOrm, Base

engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = True,
)

async_session_factory = async_sessionmaker(engine)

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def insert_data(user_id, value):
    async with async_session_factory() as session:
        session.add_all(ValuesOrm(user_id, value))
        await session.commit()