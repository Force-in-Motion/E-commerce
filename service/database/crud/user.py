from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from service.database.models import User as User_model
from web.schemas import UserInput


class UserAdapter:

    @classmethod
    async def get_users(cls, session: AsyncSession) -> list[User_model]:
        try:
            request = select(User_model).order_by(User_model.id)
            result = await session.execute(request)
            users = result.scalars().all()
            return list(users)

        except SQLAlchemyError:
            return []

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, id: int) -> User_model | None:
        try:
            return await session.get(User_model, id)

        except SQLAlchemyError:
            return None

    @classmethod
    async def add_user(cls, session: AsyncSession, user_input: UserInput) -> dict:
        try:
            user_model = User_model(**user_input.model_dump())
            session.add(user_model)
            await session.commit()
            return {"status": "ok", "detail": "User has been added"}

        except SQLAlchemyError:
            await session.rollback()
            return {"status": "False", "detail": "Error added User"}

    @classmethod
    async def update_user(
        cls,
        user_input: UserInput,
        user_model: User_model,
        session: AsyncSession,
        partial: bool = False,
    ) -> dict:
        try:
            for key, value in user_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(user_model, key, value)

            await session.commit()
            return {"status": "ok", "detail": "User has been updated"}

        except SQLAlchemyError:
            await session.rollback()
            return {"status": "False", "detail": "Error updated User"}

    @classmethod
    async def del_user(cls, user_model: User_model, session: AsyncSession) -> dict:
        try:
            await session.delete(user_model)
            await session.commit()
            return {"status": "ok", "detail": "User has been deleted"}

        except SQLAlchemyError:
            await session.rollback()
            return {"status": "False", "detail": "Error deleted User"}
