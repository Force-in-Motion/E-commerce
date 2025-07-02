from fastapi import APIRouter

from web.schemas.product import Product
from web.schemas.user import User

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def get_products() -> list[Product]:
    pass

@router.post('/')
async def add_user(user: User):
    pass