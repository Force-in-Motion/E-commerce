__all__ = ["include_router"]

from .product import router as product_router
from .user import router as user_router
from .profile import router as profile_router


def include_router(app):
    app.include_router(product_router, prefix="/product", tags=["Product"])
    app.include_router(user_router, prefix="/user", tags=["User"])
    app.include_router(profile_router, prefix="/profile", tags=["Profile"])
