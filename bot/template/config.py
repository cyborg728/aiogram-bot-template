from enum import IntEnum, auto
import os
from typing import Literal

from pydantic import Field, SecretStr
from sqlalchemy import URL
from pydantic_settings import BaseSettings

ENV_PREFIX: str = os.getenv("ENV_PREFIX", "")


class Role(IntEnum):
    """
    # TODO: can i put roles into env? Why?and do i need custom roles?
    # TODO: translate into english
    NEWBIE, SIMPLE_USER, USER стоят выше по цепочке и заменяют друг друга.
    Остальные роли как дополнения (как в дискорде)
    SUPERUSER заменяет все роли.
    """

    NEWBIE = auto()
    SIMPLE_USER = auto()
    USER = auto()  # accepted rules

    # MODERATOR = auto()
    ADMINISTRATOR = auto()
    SUPERUSER = auto()


class CustomBaseSettings(BaseSettings):
    class Config:
        # `.env.dev` takes priority over `.env`
        # env_file = ".env"
        extra = "ignore"
        env_prefix = ENV_PREFIX
        validate_default = True


class BotApiConfig(CustomBaseSettings):
    type: Literal["local", "official", "test"] = "official"
    # botapi_url: str | None
    # botapi_file_url: str | None

    # @property
    # def is_local(self) -> bool:
    #     return self.type == BotApiType.local

    # @property
    # def is_test(self) -> bool:
    #     return self.type == BotApiType.test

    # def create_server(self) -> TelegramAPIServer:
    #     if self.type != BotApiType.local:
    #         raise RuntimeError("can create only local botapi server")
    #     return TelegramAPIServer(
    #         base=f"{self.botapi_url}/bot{{token}}/{{method}}",
    #         file=f"{self.botapi_file_url}{{path}}",
    #     )

    class Config:
        env_prefix = ENV_PREFIX + "bot_api_"


class BotConfig(CustomBaseSettings):
    available_locales: list[str] = ['en', 'ru']
    bot_api: "BotApiConfig" = Field(default_factory=BotApiConfig)
    default_locale: str = "en"
    drop_pending_updates: bool = True
    enable_webhook: bool = False
    # pre_prod = imitate prod
    environment: Literal["dev", "pre_prod", "prod"] = "dev"
    logging_dir: str = "bot/template/logs/bot/"
    logging_level: int = 10
    throttling_rate_limit: float = 1.0
    token: SecretStr = SecretStr('')
    # use __post_init_post_parse__
    # bot_id: int = int("token".split(":")[0])


class DBConfig(CustomBaseSettings):
    connector: str = "asyncpg"  # asyncpg | 
    host: str = ""
    name: str = ""
    password: SecretStr = SecretStr('')
    path_to_user_model: str = "bot.template.models.user" # "bot.template.models.user" | path to YourUserModel(SQLModel). Model should be named "User"
    # TODO: ChatModel. importlib.import_module(module_name)
    # path_to_chat_model: Literal[False] | str = False # Fasle | "bot.template.models.chat" | path to YourChatModel(SQLModel). Model should be named "Chat"
    port: int = 0
    roles: type[IntEnum] = Role
    storage: Literal["postgres"] | None = None  # postgres | 
    username: str = ""

    class Config:
        env_prefix = ENV_PREFIX + "DB_"

    def create_url(self) -> URL:
        if self.storage == "postgres":
            return URL.create(
                drivername=f"{self.storage}+{self.connector}",
                username=self.username,
                password=self.password.get_secret_value(),
                host=self.host,
                port=self.port,
                database=self.name,
            )
        else:
            raise ValueError("storage is not available")


class FSMRedisConfig(CustomBaseSettings):
    data_ttl: int = 600
    db: int = 0
    host: str = ""
    password: str = ""
    port: int = 0
    state_ttl: int = 600
    username: str = ""

    class Config:
        env_prefix = ENV_PREFIX + "FSM_" + "REDIS_"


class FSMConfig(CustomBaseSettings):
    storage: Literal["memory", "redis"] = "memory"

    class Config:
        env_prefix = ENV_PREFIX + "FSM_"


class OpenAIConfig(CustomBaseSettings):
    enable_openai: bool = False
    token: str = ""
    default_model: str = ""

    class Config:
        env_prefix = ENV_PREFIX + "OPENAI_"


class Config(CustomBaseSettings):
    bot: BotConfig = Field(default_factory=BotConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    db: DBConfig = Field(default_factory=DBConfig)
    roles_instance = Role
