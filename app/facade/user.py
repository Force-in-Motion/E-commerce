from sqlalchemy.ext.asyncio import AsyncSession

from app.facade.base import BaseFacade
from app.models import User as User_model
from app.schemas import UserRequest
from app.crud import UserAdapter


class UserFacade(BaseFacade[User_model, UserRequest, UserAdapter]):

    model = User_model
    scheme = UserRequest
    adapter = UserAdapter

    @classmethod
    async def get_user_by_name(
        cls,
        name: str,
        session: AsyncSession,
    ) -> User_model:
        """
        Возвращает модель пользователя по его имени из БД
        :param name: Имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        return await cls.adapter.get_by_name(name=name, session=session)
