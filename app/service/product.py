from app.repositories import ProductRepo
from app.service import BaseService
from app.models import Product as Product_model
from app.schemas import ProductRequest


class ProductService(BaseService[Product_model, ProductRepo]):
    model = Product_model
    repo = ProductRepo
