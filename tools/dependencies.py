from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from service.database import db_connector
from service.database.models import Product as Product_model
from service.database.crud import ProductAdapter as pa


async def product_by_id(id: Annotated[int, Path], session: AsyncSession = Depends(db_connector.session_dependency)) -> Product_model:
    product_model = await pa.get_product_by_id(id, session)

    if product_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product with this id not found')

    return product_model