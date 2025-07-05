__all__ = ['include_router']

from .product import router as product_router
from .user import router as user_router

def include_router(app):
    app.include_router(product_router, prefix='/product', tags=['Products'])
    app.include_router(user_router, prefix='/users', tags=['Users'])