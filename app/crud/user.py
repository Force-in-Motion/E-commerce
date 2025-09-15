from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCrud
from app.models import User as User_model
from app.schemas import UserInput
from app.tools.custom_err import DatabaseError


class UserAdapter(BaseCrud[User_model, UserInput]):

    model = User_model
    scheme = UserInput

    @classmethod
    async def get_by_name(
        cls,
        name: str,
        session: AsyncSession,
    ) -> Optional[User_model]:
        """
        Возвращает модель пользователя по его имени из БД
        :param name: Имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        model_cls = await cls._check_model(cls.model)
        try:
            return await session.get(model_cls, name)

        except SQLAlchemyError:
            raise DatabaseError(f"{model_cls.__name__}model with this name not found")
