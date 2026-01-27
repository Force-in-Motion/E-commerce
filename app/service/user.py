from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.schemas.user import UserUpdate ,UserCreate
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
        Возвращает модель пользователя по его логину из БД
        :param name: Логин пользователя
        :param session: Асинхронная сессия
        :return: ORM модель пользователя | None
        """
        user_model = await cls.repo.get_by_login(login=login, session=session)

        return user_model if user_model is not None else None
