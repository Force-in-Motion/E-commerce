from sqlalchemy import String, Integer

from service.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    """Класс, описывающий мета информацию таблицы Product"""

    __tablename__ = "Product"  # Название таблицы в БД

    # Описание мета информации таблицы
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
