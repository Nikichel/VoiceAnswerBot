from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from config import settings
from database.models import ValuesOrm, Base
from sqlalchemy import select

class DataBaseHelper:

    def __init__(self):
        self.engine = create_async_engine(
            url = settings.DATABASE_URL_asyncpg,
            echo = False,
            poolclass=AsyncAdaptedQueuePool
        )
        self.async_session_factory = async_sessionmaker(self.engine)

    async def create_table(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def insert_data(self, user_id, value):
        async with self.async_session_factory() as session:
            existing_record = await session.execute(
                ValuesOrm.__table__.select().where(ValuesOrm.user_id == user_id, ValuesOrm.value == value)
            )
            data = existing_record.one_or_none()
            #print(data)
            if data is None:
                new_value = ValuesOrm(user_id=user_id, value=value)  # Используйте ключевые аргументы
                session.add(new_value)
                await session.commit()