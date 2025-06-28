from fastapi import APIRouter
from web.users.shemas import User
from web.users import crud

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/')
async def add_user(user: User):
    return crud.create_user(user)