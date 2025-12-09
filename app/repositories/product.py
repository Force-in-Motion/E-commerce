from app.repositories import BaseRepo
from app.models import Product as Product_model


class ProductRepo(BaseRepo[Product_model]):

    model: Product_model
