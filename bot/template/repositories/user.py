from importlib import import_module
from ..models import User
from ..repositories.abstract import Repository
from bot import config


class UserRepository(Repository[User]):
    """
    User repository for CRUD and other SQL queries
    """

    model = getattr(import_module(config.db.path_to_user_model), "User")