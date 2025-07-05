from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.database.crud import ProductAdapter as pa
from service.database import db_connector
from service.database.models import Product as Product_model
from web.schemas import ProductInput, ProductOutput
from tools import product_by_id


router = APIRouter()


@router.get('/', response_model=list[ProductOutput], status_code=status.HTTP_200_OK)
async def get_products(session: AsyncSession = Depends(db_connector.session_dependency)) -> list[ProductOutput]:

    return await pa.get_products(session)



@router.get('/{id}', response_model=ProductOutput, status_code=status.HTTP_200_OK)
async def get_product_by_id(product: ProductOutput = Depends(product_by_id)) -> ProductOutput:

    return product



@router.post('/', response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_product(product: ProductInput,
                      session: AsyncSession = Depends(db_connector.session_dependency)
                      ) -> dict:

    return await pa.add_product(product, session)



@router.put('/{id}', response_model=dict, status_code=status.HTTP_200_OK)
async def update_product(product_input: ProductInput,
                         product_model: Product_model = Depends(product_by_id),
                         session: AsyncSession = Depends(db_connector.session_dependency)
                         ) -> dict:

    return await pa.update_product(product_input, product_model, session)



@router.patch('/{id}', response_model=dict, status_code=status.HTTP_200_OK)
async def update_product(product_input: ProductInput,
                         product_model: Product_model = Depends(product_by_id),
                         session: AsyncSession = Depends(db_connector.session_dependency)
                         ) -> dict:

    return await pa.update_product(product_input, product_model, session, partial=True)



@router.delete('/{id}', response_model=dict, status_code=status.HTTP_200_OK)
async def del_product(product_model: Product_model = Depends(product_by_id),
                      session: AsyncSession = Depends(db_connector.session_dependency)
                      ) -> dict:

    return await pa.del_product(product_model, session)


