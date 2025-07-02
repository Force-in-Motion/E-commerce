from fastapi import HTTPException, status
from fastapi import APIRouter

from web.schemas.user import User as User_scheme
from service.database.crud.user import UserAdapter as ua




router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def get_users(session) -> list[User_scheme]:
    result = await ua.get_users(session)

    if result:
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The database is empty')


@router.get('/{id}')
async def get_user_by_id(session, id: int):
        result = await ua.get_user_by_id(session, id)

        if result is not None:
            return result

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User with this id not found')



@router.post('/')
async def add_user(session, user: User_scheme) -> dict:
        result = await ua.add_user(session, user)

        if result:
            return {'status': 'ok', 'detail': 'User added'}

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error adding user')


@router.put('/{id}')
async def update_user(session, id: int, user: User_scheme):
    result = await ua.update_user(session, id, user)

    if result:
        return {'status': 'ok', 'detail': 'User updated'}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Error updating user')


@router.delete('/{id}')
async def del_user_by_id(session, id: int) -> dict:
    result = await ua.del_user(session, id)

    if result:
        return {'status': 'ok', 'detail': 'User deleted'}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Error removing user')