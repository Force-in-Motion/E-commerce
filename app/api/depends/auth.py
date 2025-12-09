import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse
from app.service.user import UserFacade


class AuthUtils:


    @classmethod
    async def hash_password(password: str) -> bytes:
        """
        Хэширует полученный пароль
        :param password: Пароль в виде строки
        :return: Пароль в байтах
        """
        return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())


    @classmethod
    async def check_password(
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
    async def check_username(username: str) -> bool:
        """
        
        :param param:
        :param param:
        :return:
        """


    

    @classmethod
    def validate_user(form_data: OAuth2PasswordRequestForm = Depends()) -> UserResponse:
        """
        Выполняет валидацию пользователя, если все проверки пройдены то возвращает его
        :param form_data: При помощи Depends() создается объект OAuth2PasswordRequestForm, содержащий данные, введенные в форме клиента form_data.username и form_data.password
        :return: Пользователя
        """
        user_model = UserFacade.get_user_by_name(form_data.username)
        
        user = AuthUtils.check_username() # Проверка наличия пользователя в базе по его имени 

        if not AuthUtils.check_password(  # Сравнивает пароли: через метод validate_password хэширует полученный пароль и сравнивает с захэшированным паролем в БД
            password=form_data.password,
            hashed_password=user.password,
        ):
            raise DBExeption.unauthorized  # Если захэшированные пароли не совпадают - выбрасывает исключение

        return AuthUtils.check_user_status(user)  # Проверяет статус пользователя, если True - возвращает пользователя, иначе выбросит исключение