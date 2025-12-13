__all__ = [
    "Inspector",
    "UserAuth",
]


from app.api.depends.inspect import Inspector
from app.api.depends.user.user import UserAuth
