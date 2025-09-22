from app.crud import ProductAdapter
from app.facade import BaseFacade
from app.models import Product as Product_model
from app.schemas import ProductInput


class ProductFacade(BaseFacade[Product_model, ProductInput, ProductAdapter]):
    model: Product_model
    scheme: ProductInput
    adapter: ProductAdapter
