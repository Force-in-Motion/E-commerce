from fastapi import HTTPException
from fastapi import APIRouter

from web.shemas.user import User
from service.database.crud.user import UserAdapter




router = APIRouter(prefix='/users', tags=['users'])


@router.post('/')
async def add_user(session, user: User) -> dict:
    try:
        await UserAdapter.add_user(session, user)
        return {'status': 'ok', 'status_code': 200}

    except HTTPException as e:
        return {'status': e}
