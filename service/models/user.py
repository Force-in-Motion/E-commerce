from sqlalchemy.orm import Mapped
from service.models.base import Base



class User(Base):
    id: Mapped[int]
    name: Mapped[str]
    floor: Mapped[str]
    age: Mapped[int]
    email: Mapped