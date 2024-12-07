from aiogram import BaseMiddleware


class I18nMiddleware(BaseMiddleware):
    def __init__(self, i18n: I18n = I18n()) -> None:
        self.i18n = i18n

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data["db"].current_user
        with I18nContext.with_current(
            self.new_context(
                locale=cast(str, locale or self.core.default_locale),
                data=data,
            )
        ) as context:
            data[self.context_key] = context
            yield context



from aiogram.utils.mixins import ContextInstanceMixin
from aiogram.utils.i18n.middleware import FSMI18nMiddleware
from aiogram.utils.i18n import I18n