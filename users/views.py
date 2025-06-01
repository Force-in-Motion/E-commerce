from typing import Annotated
from fastapi import APIRouter
from users.shemas import User
from users import crud

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/')
async def add_user(user: User):
    return crud.create_user(user)