from app.crud import OrderAdapter
from app.facade import BaseFacade
from app.models import Order as Order_model
from app.schemas import OrderInput


class ProductFacade(BaseFacade[Order_model, OrderInput, OrderAdapter]):
    model: Order_model
    scheme: OrderInput
    adapter: OrderAdapter
