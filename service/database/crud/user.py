from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from service.database.models.user import User
from web.shemas.user import User as User_object


class UserAdapter:

    @classmethod
    async def get_users(cls, session: AsyncSession) -> list[User]:
        try:
            request = select(User).order_by(User.id)
            result = await session.execute(request)
            users = result.scalars().all()
            return list(users)

        except SQLAlchemyError as e:
            print('Ошибка при получении списка всех пользователей')
            return []


    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, id: int) -> User | None:
        try:
            return await session.get(User, id)

        except SQLAlchemyError as e:
            print('Ошибка при получении пользователя по id')
            return None


    @classmethod
    async def add_user(cls, session: AsyncSession, user: User_object) -> bool:
        try:
            user = User(**user.model_dump())
            session.add(user)
            await session.commit()
            return True

        except SQLAlchemyError as e:
            print('Ошибка при добавлении пользователя')
            await session.rollback()
            return False


    @classmethod
    async def update_user(cls, session: AsyncSession, id: int, data) -> bool:
        pass


    @classmethod
    async def del_user(cls, session: AsyncSession, id: int) -> bool:
        try:
            user = await session.get(User, id)
            if user is None:
                return False

            await session.delete(user)
            await session.commit()
            return True

        except SQLAlchemyError as e:
            print('Ошибка при удалении пользователя')
            await session.rollback()
            return False
