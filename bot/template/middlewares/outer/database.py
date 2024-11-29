from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.exc import DBAPIError

from ...storages.postgres.storage import Database, get_sessionmaker


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        pool = await get_sessionmaker()

        async with pool() as session:
            async with session.begin() as transaction:
                try:
                    data["db"] = Database(session)

                    result = await handler(event, data)

                    # TODO: проверить: Если во вложенной транзакции сделаю коммит, то будет ли здесь что-то?
                    print("CHECKING: session.new, session.dirty, session.deleted")
                    print(session.new, session.dirty, session.deleted)
                    if session.new or session.dirty or session.deleted:
                        print("YEAH! COMMITED!")
                        await transaction.commit()
                    else:
                        print("NOT COMMITED!")

                    return result
                except DBAPIError:
                    await transaction.rollback()
                    raise
                except Exception:
                    await transaction.rollback()
                    raise
                finally:
                    await session.close()