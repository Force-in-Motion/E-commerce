from service.models.base import Base
from sqlalchemy.orm import Mapped



class Product(Base):
    __tablename__ = 'Product'

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]