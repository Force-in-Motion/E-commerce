from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCrud
from app.models import (
    Cart as Cart_model,
    CartProduct as Association_model,
    Product as Product_model,
)
from app.schemas import CartRequest
from app.tools import DatabaseError


class CartAdapter(BaseCrud[Cart_model, CartRequest]):
    pass
