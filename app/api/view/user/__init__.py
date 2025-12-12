from app.api.view.user.post import router as post_router
from app.api.view.user.user import router as user_router
from app.api.view.user.cart import router as cart_router
from app.api.view.user.order import router as order_router
from app.api.view.user.product import router as product_router
from app.api.view.user.profile import router as profile_router


def include_user_routers(app):
    app.include_router(post_router)
    app.include_router(user_router)
    app.include_router(cart_router)
    app.include_router(order_router)
    app.include_router(product_router)
    app.include_router(profile_router)



    