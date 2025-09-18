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
        try:
            return await session.get(cls.model, name)

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Database operation failed for {cls.model.__name__}"
            ) from e
