from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.exc import DBAPIError

from ...storages.postgres.storage import Database, get_sessionmaker


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        pool = await get_sessionmaker()
        session = None

        try:
            async with pool() as session:
                async with session.begin() as transaction:
                    try:
                        data["db"] = Database(session)

                        result = await handler(event, data)

                        # TODO: check if this is needed
                        if session.new or session.dirty or session.deleted:
                            await transaction.commit()
                        else:
                            print("NOT COMMITED!")

                        return result
                    except DBAPIError:
                        await transaction.rollback()
                    except Exception:
                        await transaction.rollback()
                        raise
        finally:
            if session is not None:
                await session.close()
