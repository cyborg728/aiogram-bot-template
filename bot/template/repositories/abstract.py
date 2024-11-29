from abc import abstractmethod
from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import ColumnExpressionArgument
from sqlmodel import SQLModel

# TODO: check is right or not?
AbstractModel = TypeVar("AbstractModel", bound=SQLModel)


class Repository(Generic[AbstractModel]):
    """
    Repository abstract class
    :param model: Which model will be used for operations
    """

    model: Type[AbstractModel]

    def __init__(self, session: AsyncSession):
        """
        Initialize abstract repository class
        :param session: Session in which repository will work
        """
        self.session = session

    async def create(
        self,
        **kwargs: Any,
    ) -> AbstractModel:
        entity = self.model(**kwargs)

        self.session.add(entity)

        return entity

    async def delete(self, *whereclause: ColumnExpressionArgument) -> None:
        """
        Delete from the database

        :param whereclause: (Optional) Which statement
        :return: Nothing
        """
        await self.session.delete(await self.get_by_where(*whereclause))

    async def get(self, ident: Any) -> AbstractModel:
        """
        Get an ONE model from the database with PK
        :param ident: Key which need to find entry in database
        :return:
        """
        result = await self.session.get(entity=self.model, ident=ident)

        if not result:
            raise NoResultFound(f"{self.model.__name__} with {ident} ident not found!")

        return result

    async def get_by_where(
        self, *whereclause: ColumnExpressionArgument
    ) -> AbstractModel | None:
        """
        Get an ONE model from the database with whereclause
        :param whereclause: Clause by which entry will be found
        :return: Model if only one model was found, else None
        """
        result = await self.session.execute(select(self.model).where(*whereclause))

        # TODO: check return Model if only one model was found, else None
        return result.scalar_one()

    async def get_many(
        self, *whereclause: ColumnExpressionArgument, limit: int = 100, order_by=None
    ) -> Sequence[AbstractModel]:
        """
        Get many models from the database with whereclause
        :param whereclause: Where clause for finding models
        :param limit: (Optional) Limit count of results
        :param order_by: (Optional) Order by clause

        Example:
        # TODO: check example "==" and "="
        >> Repository.get_many(Model.id == 1, limit=10, order_by=Model.id)

        :return: List of founded models
        """
        statement = select(self.model).where(*whereclause).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)
        result = await self.session.execute(statement)

        return result.scalars().all()

    @abstractmethod
    async def get_or_create(self, instance: AbstractModel) -> AbstractModel:
        """
        :return: AbstractModel
        """
        raise NotImplementedError
