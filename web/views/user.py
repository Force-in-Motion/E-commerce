from fastapi import HTTPException
from fastapi import APIRouter
from sqlalchemy.util import await_only

from web.shemas.user import User
from service.database.crud.user import UserAdapter




router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def get_users(session):
    try:
        return await UserAdapter.get_users(session)

    except HTTPException as e:
        return {'status': e}


@router.get('/{id}')
async def get_user_by_id(session, id: int):
    try:
        return await UserAdapter.get_user_by_id(session, id)

    except HTTPException as e:
        return {'status': e}


@router.post('/')
async def add_user(session, user: User) -> dict:
    try:
        await UserAdapter.add_user(session, user)
        return {'status': 'ok', 'status_code': 200}

    except HTTPException as e:
        return {'status': e}


@router.delete('/{id}')
async def del_user_by_id(session, id: int):
    try:
        await UserAdapter.del_user(session, id)
        return {'status': 'ok', 'status_code': 200}

    except HTTPException as e:
        return {'status': e}