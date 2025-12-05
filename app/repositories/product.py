from app.repositories import BaseCrud
from app.models import Product as Product_model


class ProductAdapter(BaseCrud[Product_model]):

    model: Product_model
