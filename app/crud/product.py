from app.crud import BaseCrud
from app.models import Product as Product_model
from app.schemas import ProductRequest


class ProductAdapter(BaseCrud[Product_model, ProductRequest]):

    model: Product_model
    scheme: ProductRequest
