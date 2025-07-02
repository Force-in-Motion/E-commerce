from fastapi import APIRouter, HTTPException, status

from service.database.crud.product import ProductAdapter as pd
from web.schemas.product import Product as Product_scheme
from service.database.models.product import Product as Product_model

router = APIRouter(prefix='/product', tags=['users'])


@router.get('/')
async def get_products(session) -> list[Product_model]:
    result = await pd.get_products(session)

    if result:
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The database is empty')


@router.get('/{id}')
async def get_product_by_id(session, id: int) -> Product_model:
    result = await pd.get_product_by_id(id, session)

    if result is not None:
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product with this id not found')



@router.post('/')
async def add_product(session, product: Product_scheme):
    result = await pd.add_product(product, session)

    if result:
        return {'status': 'ok', 'detail': 'Product added'}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error adding product')


@router.put('/{id}')
async def update_product(session, id: int, product: Product_scheme):
    result = await pd.update_product(id, product, session)

    if  result:
        return {'status': 'ok', 'detail': 'Product updated'}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error updating product')


@router.delete('/{id}')
async def del_product(session, id: int):
    result = await pd.del_product(id, session)

    if result is not None:
        return {'status': 'ok', 'detail': 'Product deleted'}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error removing product')