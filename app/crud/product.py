from app.crud import BaseCrud
from app.models import Product as Product_model
from app.schemas import ProductInput


class ProductAdapter(BaseCrud[Product_model, ProductInput]):

    model: Product_model
    scheme: ProductInput
