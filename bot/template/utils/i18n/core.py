from pathlib import Path

from aiogram.utils.mixins import ContextInstanceMixin
from fluent_compiler.bundle import FluentBundle

from bot import config


class I18n(ContextInstanceMixin["I18n"]):
    _translator_hub: dict[str, FluentBundle]

    def __init__(
        self,
        locale: str = config.bot.default_locale,
        locales: 
    ) -> None:
        self._locale = locale
        self._translator_hub = {}
        self._init_translator_hub()

    def _init_translator_hub(self) -> None:
        self._translator_hub = {}

        for language_code in config.bot.supported_locales:
            files = ["locales/" + (language_code + ".ftl") + "/messages.ftl"]
            self._translator_hub[language_code.value] = FluentTranslator(
                locale=language_code.value,
                translator=FluentBundle.from_files(
                    language_code.value, files, use_isolating=False
                ),
            )

    async def startup(self) -> None:
        self.locales.update(self.find_locales())

    async def shutdown(self) -> None:
        self.locales.clear()
