from app.crud import ProductAdapter
from app.facade import BaseFacade
from app.models import Product as Product_model
from app.schemas import ProductRequest


class ProductFacade(BaseFacade[Product_model, ProductAdapter]):
    model = Product_model
    adapter = ProductAdapter
