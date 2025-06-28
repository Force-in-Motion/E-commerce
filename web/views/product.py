from fastapi import APIRouter
from web.shemas.user import User

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def get_users() -> list[User]:


@router.post('/')
async def add_user(user: User):
    return crud.create_user(user)