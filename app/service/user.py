from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.service.base import BaseService
from app.models import User as User_model
from app.repositories import UserRepo


class UserService(BaseService[UserRepo]):

    repo = UserRepo

    @classmethod
    async def get_user_by_login(
        cls,
        login: EmailStr,
        session: AsyncSession,
    ) -> Optional[User_model]:
        """
        Возвращает модель пользователя по его имени из БД
        :param name: Имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        user_model = await cls.repo.get_by_login(login=login, session=session)

        return user_model if user_model else None
