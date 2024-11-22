from datetime import datetime
from sqlalchemy.sql.sqltypes import DATETIME_TIMEZONE
from sqlalchemy.sql.schema import Column
from sqlmodel import Field, SQLModel

class BaseModel(SQLModel):
    __mapper_args__ = {"eager_defaults": True}
    # When eager_defaults=True is set on a session or query, SQLAlchemy will automatically fetch the values of columns with server-side defaults or server-generated values immediately after an INSERT or UPDATE operation. This ensures that the in-memory state of the objects is consistent with what is in the database.


class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(
            DATETIME_TIMEZONE,
            nullable=False,
        ),
    )
    # TODO: test onupdata
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(
            DATETIME_TIMEZONE,
            nullable=False,
            onupdate=datetime.now,
        ),
    )
