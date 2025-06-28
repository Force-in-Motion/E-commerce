from sqlalchemy import select
from service.database.models.user import User



async def get_users(session) -> list[User]:
    request = select()


async def get_user_by_id(id: int) -> User:
    pass


async def create_user(user: User) -> bool:
    pass


async def update_user(id: int, data) -> bool:
    pass


async def del_user(id: int) -> bool:
    pass