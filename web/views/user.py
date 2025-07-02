from fastapi import HTTPException, status
from fastapi import APIRouter

from web.schemas.user import User
from service.database.crud.user import UserAdapter




router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def get_users(session) -> list[User]:

    result = await UserAdapter.get_users(session)

    if result:
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='База данных пуста')


@router.get('/{id}')
async def get_user_by_id(session, id: int):

        result = await UserAdapter.get_user_by_id(session, id)

        if result is not None:
            return result

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь с таким id не найден')



@router.post('/')
async def add_user(session, user: User) -> dict:

        result = await UserAdapter.add_user(session, user)

        if result:
            return {'status': 'ok', 'detail': 'User added'}

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Ошибка при добавлении пользователя')


@router.delete('/{id}')
async def del_user_by_id(session, id: int) -> dict:

    result = await UserAdapter.del_user(session, id)

    if result:
        return {'status': 'ok', 'detail': 'User deleted'}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь с таким id не найден')