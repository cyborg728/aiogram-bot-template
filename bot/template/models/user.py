

from typing import Callable, ClassVar, Union
from sqlalchemy.sql.schema import Column
from ..storages.postgres.ext.pgsql_uuid7 import uuid7
from sqlalchemy.sql.sqltypes import ARRAY, BigInteger, Enum as SA_Enum, UUID as SA_UUID, String, Interval, Boolean
from sqlmodel import Field, SQLModel
from uuid import UUID

from .base import BaseModel, TimestampMixin
from datetime import timedelta
from aiogram.types import User as tg_User
from sqlalchemy.event.api import listens_for
from bot import config
from ...constants import Role


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
        sa_column=Column(SA_UUID, nullable=False, unique=True, primary_key=True,),
    )

    roles: list[Role] = Field(
        default=[Role.NEWBIE],
        sa_column=Column(
            ARRAY(SA_Enum(Role)),
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

    blocked: bool = Field(
        default=False,
        sa_column=Column(
            Boolean,
            nullable=False,
        ),
    )


@listens_for(User.roles, "set", retval=True)
def roles_validation(target, value: list[Role], oldvalue, initiator) -> list[Role]:
    """
    Validates the list of roles for a User:
    - If more than one role is set:
        - If SUPERUSER is in the list, only SUPERUSER is allowed.
        - Otherwise, NEWBIE is removed if present.
    """
    if len(value) > 1:
        if Role.SUPERUSER in value:
            # Enforce only SUPERUSER
            value = [Role.SUPERUSER]
        else:
            # Remove NEWBIE if present
            value = [role for role in value if role != Role.NEWBIE]

    return value