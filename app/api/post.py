from datetime import datetime

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.facade.post import PostFacade
from app.schemas import PostOutput, PostInput
from app.tools import Inspector

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/all",
    response_model=list[PostOutput],
    status_code=status.HTTP_200_OK,
)
async def get_all_posts(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[PostOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список всех постов пользователей
    """
    return await PostFacade.get_all_models(session=session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/date",
    response_model=list[PostOutput],
    status_code=status.HTTP_201_CREATED,
)
async def get_posts_by_date(
    dates: tuple[datetime, datetime] = Depends(Inspector.date_checker),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[PostOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов пользователей, добавленных за указанный интервал времени
    :param dates: кортеж, содержащий начало интервала времени и его окончание
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех постов, созданных за указанный интервал времени
    """
    return await PostFacade.get_models_by_date(
        dates=dates,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/by-id/{post_id}",
    response_model=PostOutput,
    status_code=status.HTTP_200_OK,
)
async def get_post_by_id(
    post_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> PostOutput:
    """
     Обрабатывает запрос с фронт энда на получение конкретного поста по его id
    :param post_id: объект PostOutput, который получается путем выполнения зависимости (метода post_by_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: конкретный пост по его id
    """
    return await PostFacade.get_model_by_id(
        model_id=post_id,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/by-user/{user_id}",
    response_model=list[PostOutput],
    status_code=status.HTTP_200_OK,
)
async def get_posts_by_user_id(
    user_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[PostOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов конкретного пользователя
    :param user_id: список объектов PostOutput, который получается путем выполнения зависимости (метода posts_by_user_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех постов пользователя
    """
    return await PostFacade.get_models_by_user_id(
        user_id=user_id,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post(
    "/by-user/{user_id}",
    response_model=PostOutput,
    status_code=status.HTTP_201_CREATED,
)
async def register_post(
    user_id: int,
    post_in: PostInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> PostOutput:
    """
    Обрабатывает запрос с фронт энда на добавление нового поста пользователя в БД
    :param post_in: PostInput - объект, содержащий данные поста пользователя
    :param user_id: UserModel - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostFacade.register_model_by_user_id(
        user_id=user_id,
        post_in=post_in,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put(
    "/by-id/{post_id}",
    response_model=PostOutput,
    status_code=status.HTTP_200_OK,
)
async def full_update_post(
    post_id: int,
    post_in: PostInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> PostOutput:
    """
    Обрабатывает запрос с фронт энда на полное обновление конкретного поста пользователя в БД
    :param post_in:  PostInput - объект, содержащий данные поста пользователя
    :param post_id: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostFacade.update_model(
        model_id=post_id,
        post_in=post_in,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/by-id/{post_id}",
    response_model=PostOutput,
    status_code=status.HTTP_200_OK,
)
async def partial_update_post(
    post_id: int,
    post_in: PostInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> PostOutput:
    """
    Обрабатывает запрос с фронт энда на частичное обновление конкретного поста пользователя в БД
    :param post_in:  PostInput - объект, содержащий данные поста пользователя
    :param post_id: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostFacade.update_model(
        model_id=post_id,
        post_in=post_in,
        session=session,
        partial=True,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_posts(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех постов пользователей из БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostFacade.clear_table(session=session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/by-id/{post_id}",
    response_model=PostOutput,
    status_code=status.HTTP_200_OK,
)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> PostOutput:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного поста пользователя из БД
    :param post_id: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return:
    """
    return await PostFacade.delete_model(
        model_id=post_id,
        session=session,
    )
