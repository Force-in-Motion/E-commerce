from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from service.database.models.base import Base



class User(Base):

    __tablename__ = 'User'

    name: Mapped[str] = mapped_column(String, nullable=False)
    floor: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)