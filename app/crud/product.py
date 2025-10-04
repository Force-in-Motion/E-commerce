from app.crud import BaseCrud
from app.models import Product as Product_model
from app.schemas import ProductRequest


class ProductAdapter(BaseCrud[Product_model]):

    model: Product_model
