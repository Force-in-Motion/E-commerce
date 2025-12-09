from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.base import BaseService
from app.models import User as User_model
from app.repositories import UserRepo


class UserService(BaseService[User_model, UserRepo]):

    model = User_model
    repo = UserRepo

    @classmethod
    async def get_user_by_login(
        cls,
        login: EmailStr,
        session: AsyncSession,
    ) -> User_model:
        """
        Возвращает модель пользователя по его имени из БД
        :param name: Имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        return await cls.repo.get_by_login(login=login, session=session)
