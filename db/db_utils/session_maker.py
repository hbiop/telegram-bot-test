from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config_reader import config

engine = create_async_engine(
    config.database_url,
    echo=False,
    pool_size=10,
    max_overflow=20
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)