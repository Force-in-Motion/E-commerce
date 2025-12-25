from app.repositories import ProductRepo
from app.service import BaseService
from app.models import Product as Product_model
from app.schemas import ProductCreate


class ProductService(BaseService[ProductRepo]):

    repo = ProductRepo
