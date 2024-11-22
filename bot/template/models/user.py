

from typing import Callable, ClassVar, Union
from sqlalchemy.sql.schema import Column
from bot import config
from ..storages.postgres.ext.pgsql_uuid7 import uuid7
from sqlalchemy.sql.sqltypes import ARRAY, BigInteger, Enum as sa_Enum, UUID as sa_UUID, String, Interval
from sqlmodel import Field, SQLModel
from uuid import UUID

from .base import BaseModel, TimestampMixin
from bot import config, Role
from datetime import timedelta
from aiogram.types import User as tg_User


class UserCreate(SQLModel):
    tguid: int = Field(
        sa_column=Column(BigInteger, nullable=False, unique=True, index=True),
    )

    language_code: str = Field(
        default=config.bot.default_locale,
        sa_column=Column(
            String,
            nullable=False,
        )
    )

    @classmethod
    def from_aiogram(cls, user: tg_User) -> "UserCreate":
        return cls(
            tguid=user.id,
            language_code=user.language_code or config.bot.default_locale,
        )


class User(TimestampMixin, UserCreate, BaseModel, SQLModel, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "user"

    user_id: UUID = Field(
        default_factory=uuid7,
        sa_column=Column(sa_UUID, nullable=False, unique=True, primary_key=True,),
    )

    roles: list[Role] = Field(
        default=[Role.NEWBIE],
        sa_column=Column(
            ARRAY(sa_Enum(Role)),
            nullable=False,
        ),
    )

    utc_offset: timedelta = Field(
        default_factory=timedelta,
        sa_column=Column(
            Interval,
            nullable=False,
        ),
    )
