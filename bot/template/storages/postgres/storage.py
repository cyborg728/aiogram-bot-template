from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot import config
from ...models import User
from ...repositories.user import UserRepository
from .ext.pgsql_uuid7 import uuid7



def build_connection_URL() -> URL:
    """
    This function build a connection string
    """
    return URL.create(
        drivername="postgresql+" + config.db.connector,
        username=config.db.username,
        password=config.db.password.get_secret_value(),
        host=config.db.host,
        port=config.db.port,
        database=config.db.name,
        # query={},
    )


def get_engine() -> AsyncEngine:
    return create_async_engine(
        url=build_connection_URL(),
        echo=True
        if (config.bot.environment == "dev") & (config.bot.logging_level == 10)
        else False,
        # pool_size=0, # 5 by default
    )


async def get_sessionmaker(
    engine: AsyncEngine = get_engine(),
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        autobegin=False,
        autoflush=False,
        autocommit=False,
        expire_on_commit=True,
    )


class Database:
    _user_repository: UserRepository | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    current_user: User

    @property
    def user(self) -> UserRepository:
        if self._user_repository is None:
            self._user_repository = UserRepository(session=self.session)

        return self._user_repository
