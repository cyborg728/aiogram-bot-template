from .template.config import Config, Role as default_Role

Role = default_Role

# TODO: add into README "You can create custom Role class here if you need"
# TODO: add into README "you can add some ur config right here to avoid any conflicts"

config = Config()


__all__ = ["config"]