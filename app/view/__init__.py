__all__ = ["include_router"]

from app.view.cart import router as cart_router
from app.view.order import router as order_router
from app.view.post import router as post_router
from app.view.product import router as product_router
from app.view.profile import router as profile_router
from app.view.user import router as user_router


def include_router(app):
    app.include_router(product_router, prefix="/product", tags=["Product"])
    app.include_router(user_router, prefix="/user", tags=["User"])
    app.include_router(profile_router, prefix="/profile", tags=["Profile"])
    app.include_router(post_router, prefix="/post", tags=["Post"])
    app.include_router(order_router, prefix="/order", tags=["Order"])
    app.include_router(cart_router, prefix="/cart", tags=["Cart"])
