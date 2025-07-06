from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from web.schemas.user import UserOutput, UserInput
from service.database.crud import UserAdapter as ua
from service.database.models import User as User_model
from service.database import db_connector
from tools import user_by_id


router = APIRouter()


@router.get("/", response_model=list[UserOutput], status_code=status.HTTP_200_OK)
async def get_users(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[UserOutput]:

    return await ua.get_users(session)


@router.get("/{id}", response_model=UserOutput, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user: UserOutput = Depends(user_by_id),
) -> UserOutput:

    return user


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_user(
    user: UserInput, session: AsyncSession = Depends(db_connector.session_dependency)
) -> dict:

    return await ua.add_user(session, user)


@router.put("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_user(
    user_input: UserInput,
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict:

    return await ua.update_user(user_input, user_model, session)


@router.patch("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_product(
    user_input: UserInput,
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict:

    return await ua.update_user(user_input, user_model, session, partial=True)


@router.delete("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def del_user_by_id(
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict:

    return await ua.del_user(user_model, session)
