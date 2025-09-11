__all__ = [
    "BaseCrud",
    "UserAdapter",
    "ProductAdapter",
    "ProfileAdapter",
    "PostAdapter",
    "OrderAdapter",
]

from app.interface.crud import BaseCrud
from .post import PostAdapter
from .product import ProductAdapter
from .profile import ProfileAdapter
from .user import UserAdapter
from .order import OrderAdapter
