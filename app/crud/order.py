from app.crud import BaseCrud
from app.models import Order as Order_model
from app.schemas.order import OrderInput


class OrderAdapter(BaseCrud[Order_model, OrderInput]):

    model: Order_model
    scheme: OrderInput
