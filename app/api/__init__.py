__all__ = ["include_router"]

from app.api.cart import router as cart_router
from app.api.order import router as order_router
from app.api.post import router as post_router
from app.api.product import router as product_router
from app.api.profile import router as profile_router
from app.api.user import router as user_router


def include_router(app):
    app.include_router(product_router, prefix="/product", tags=["Product"])
    app.include_router(user_router, prefix="/user", tags=["User"])
    app.include_router(profile_router, prefix="/profile", tags=["Profile"])
    app.include_router(post_router, prefix="/post", tags=["Post"])
    app.include_router(order_router, prefix="/order", tags=["Order"])
    app.include_router(cart_router, prefix="/cart", tags=["Cart"])
