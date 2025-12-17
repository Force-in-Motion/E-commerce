__all__ = [
    "Inspector",
    "UserAuth",
    "UserAuth",
    "UserCrud",
    "ProfileCrud",
    "PostCrud",
]


from app.api.depends.inspect import Inspector
from app.api.depends.user import UserAuth
from app.api.depends.user import UserAuth, UserCrud
from app.api.depends.profile import ProfileCrud
from app.api.depends.post import PostCrud
