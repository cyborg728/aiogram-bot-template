from enum import IntEnum, auto


class Role(IntEnum):
    """
    # TODO: can i put roles into env? Why?and do i need custom roles?
    # TODO: translate into english
    NEWBIE, USER заменяют друг друга.
    Остальные роли как дополнения (как в дискорде)
    SUPERUSER заменяет все роли.
    """

    NEWBIE = auto()
    USER = auto()  # accepted rules

    # MODERATOR = auto()
    ADMINISTRATOR = auto()
    SUPERUSER = auto()
    