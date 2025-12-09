import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr
from app.models.user import User as User_model
from app.schemas.user import UserCreate, UserResponse
from app.service.user import UserService
from app.tools import HTTPExeption


class AuthUtils:

    @classmethod
    async def hash_password(cls, password: str) -> bytes:
        """
        Хэширует полученный пароль
        :param password: Пароль в виде строки
        :return: Пароль в байтах
        """
        return bcrypt.hashpw(
            password=password.encode(),
            salt=bcrypt.gensalt(),
        )

    @classmethod
    async def check_password(
        cls, 
        password: str,
        hash_password,
    ) -> bool:
        """
        Сравнивает полученный пароль пользователя с захешированным его паролем из БД
        :param password: Полученный от пользователя пароль
        :param hash_password: Пароль пользователя из БД
        :return: bool
        """
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hash_password,
        )
    

    @classmethod
    async def check_user_login(cls, login: EmailStr,) -> User_model:
        """

        :param param:
        :param param:
        :return:
        """
        user_model = await UserService.get_user_by_login(login=login)

        if not user_model:
            raise HTTPExeption.unauthorized

        return user_model

    @classmethod
    async def check_user_status(cls, user_model: User_model,) -> bool:
        """

        :param param:
        :param param:
        :return:
        """
        if not user_model.is_active:
            raise HTTPExeption.user_inactive

        return user_model.is_active
    
    @classmethod
    def validate_user(cls, form_data: OAuth2PasswordRequestForm = Depends()) -> UserResponse:
        """
        Выполняет валидацию пользователя, если все проверки пройдены то возвращает его
        :param form_data: При помощи Depends() создается объект OAuth2PasswordRequestForm, содержащий данные, введенные в форме клиента form_data.username и form_data.password
        :return: Пользователя
        """
        user_model = cls.check_user_login(form_data.username)

        if not cls.check_password(
            password=form_data.password,
            hashed_password=user_model.password
        ):
            raise HTTPExeption.unauthorized

        return cls.check_user_status(user_model=user_model)