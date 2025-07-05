from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.database.crud import ProductAdapter as pa
from service.database import db_connector
from web.schemas import ProductInput, ProductOutput

router = APIRouter()


@router.get('/', response_model=list[ProductOutput])
async def get_products(session: AsyncSession = Depends(db_connector.session_dependency)) -> list[ProductOutput]:

    result = await pa.get_products(session)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The database is empty')

    return result


@router.get('/{id}', response_model=ProductOutput)
async def get_product_by_id(id: int, session: AsyncSession = Depends(db_connector.session_dependency)) -> ProductOutput:

    result = await pa.get_product_by_id(id, session)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product with this id not found')

    return result


@router.post('/', response_model=dict)
async def add_product(product: ProductInput, session: AsyncSession = Depends(db_connector.session_dependency)) -> dict:

    result = await pa.add_product(product, session)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error adding product')

    return {'status': 'ok', 'detail': 'Product added'}


@router.put('/{id}', response_model=dict)
async def update_product(id: int, product: ProductInput, session: AsyncSession = Depends(db_connector.session_dependency)) -> dict:

    result = await pa.update_product(id, product, session)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Error updating product')

    return {'status': 'ok', 'detail': 'Product updated'}


@router.delete('/{id}', response_model=dict)
async def del_product(id: int, session: AsyncSession = Depends(db_connector.session_dependency)) -> dict:

    result = await pa.del_product(id, session)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Error removing product')

    return {'status': 'ok', 'detail': 'Product deleted'}

