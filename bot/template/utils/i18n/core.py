from calendar import c
from pathlib import Path

from aiogram.utils.mixins import ContextInstanceMixin
from fluent_compiler.bundle import FluentBundle

from bot import config


class I18n(ContextInstanceMixin["I18n"]):
    _translator_hub: dict[str, FluentBundle]

    def __init__(
        self,
        locale: str = config.bot.default_locale,
        locales: list[str] = config.bot.available_locales,
    ) -> None:
        self._locale = locale
        self._translator_hub = {}
        self._init_translator_hub()

    def _init_translator_hub(self) -> None:
        self._translator_hub = {}

        for language_code in config.bot.available_locales:
            files = ["locales/" + (language_code + ".ftl") + "/messages.ftl"]
            self._translator_hub[language_code] = FluentBundle.from_files(
                language_code, files, use_isolating=False
            )

    async def startup(self) -> None:
        self.locales.update(self.find_locales())

    async def shutdown(self) -> None:
        self.locales.clear()
