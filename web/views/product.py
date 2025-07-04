from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.database.crud.product import ProductAdapter as pa
from service.database.db_connection import db_connector
from web.schemas.product import ProductInput, ProductOutput
from service.database.models.product import Product as Product_model

router = APIRouter(prefix='/product', tags=['Products'])


@router.get('/', response_model=list[ProductOutput])
async def get_products(session: AsyncSession = Depends(db_connector.session_dependency)) -> list[ProductOutput]:

    result = await pa.get_products(session)

    if result:
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The database is empty')


@router.get('/{id}', response_model=ProductOutput)
async def get_product_by_id(id: int, session: AsyncSession = Depends(db_connector.session_dependency)) -> ProductOutput:

    result = await pa.get_product_by_id(id, session)

    if result is not None:
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product with this id not found')


@router.post('/', response_model=dict)
async def add_product(product: ProductInput, session: AsyncSession = Depends(db_connector.session_dependency)) -> dict:

    result = await pa.add_product(product, session)

    if result:
        return {'status': 'ok', 'detail': 'Product added'}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error adding product')


@router.put('/{id}', response_model=dict)
async def update_product(id: int, product: ProductInput, session: AsyncSession = Depends(db_connector.session_dependency)) -> dict:

    result = await pa.update_product(id, product, session)

    if  result:
        return {'status': 'ok', 'detail': 'Product updated'}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error updating product')


@router.delete('/{id}', response_model=dict)
async def del_product(id: int, session: AsyncSession = Depends(db_connector.session_dependency)) -> dict:
    result = await pa.del_product(id, session)

    if result is not None:
        return {'status': 'ok', 'detail': 'Product deleted'}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error removing product')