from ..repositories.abstract import Repository
from datetime import timedelta
from bot.presets import User, Role


class UserRepository(Repository[User]):
    """
    User repository for CRUD and other SQL queries
    """

    model = User

    async def add_role(
        self,
        role: Role,
        user: User,
    ) -> None:
        if role not in user.roles:
            user.roles.append(role)

    async def remove_role(
        self,
        role: Role,
        user: User,
    ) -> None:
        if role in user.roles:
            await self.set_roles(
                roles=[r for r in user.roles if r != role],
                user=user,
            )

    async def set_role(self, role: Role, user: User) -> None:
        await self.set_roles(roles=[role], user=user)

    async def set_role_newbie(self, user: User) -> None:
        await self.set_role(role=Role.NEWBIE, user=user)

    async def set_roles(self, roles: list[Role], user: User) -> None:
        user.roles = roles

    async def set_utc_offset(self, utc_offset: float, user: User) -> None:
        """
        Set users utc offset in hours
        :param utc_offset: UTC offset in hours
        :param user: User which need to update
        """
        user.utc_offset = timedelta(hours=utc_offset)

    async def set_language_code(self, language_code: str, user: User) -> None:
        if user.language_code != language_code:
            user.language_code = language_code

    async def get_or_create(self, instance: User) -> User:
        """
        :return: AbstractModel
        """
        raise NotImplementedError