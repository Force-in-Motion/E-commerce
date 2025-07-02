from sqlalchemy import String, Integer

from service.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):

    __tablename__ = 'Product'

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)