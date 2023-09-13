from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from ..config import Settings, settings
from .models import Base


class DatabaseManager:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.engine = create_async_engine(
            self.settings.SQLALCHEMY_DATABASE_URI, echo=True, pool_pre_ping=True
        )
        self.session_factory = async_sessionmaker(
            self.engine, expire_on_commit=False
        )

    async def get_session(self) -> Callable[..., AsyncSession]:
        session: AsyncSession = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def init_models(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db = DatabaseManager(settings)
