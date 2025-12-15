__all__ = [
    "UserAuth",
    "UserCrud",
    "ProfileDepends",
    "PostCrud",
]

from app.api.depends.user.user import UserAuth, UserCrud
from app.api.depends.user.profile import ProfileDepends
from app.api.depends.user.post import PostCrud
