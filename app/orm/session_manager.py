from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.settings import settings

DB_URL = settings.get_db_url()
DEBUG = bool(settings.DEBUG)

engine = create_async_engine(url=DB_URL, echo=DEBUG)
async_session_maker = async_sessionmaker(bind=engine)

async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise