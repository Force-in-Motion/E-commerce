from datetime import datetime

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.facade.product import ProductFacade
from app.schemas import ProductInput, ProductOutput
from app.tools import Inspector

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов ProductOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/",
    response_model=list[ProductOutput],
    status_code=status.HTTP_200_OK,
)
async def get_all_products(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[ProductOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех продуктов
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: list[ProductOutput]
    """
    return await ProductFacade.get_all_models(session=session)


@router.get(
    "/date",
    response_model=list[ProductOutput],
    status_code=status.HTTP_200_OK,
)
async def get_products_by_date(
    dates: tuple[datetime, datetime] = Depends(Inspector.date_checker),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[ProductOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех продуктов, добавленных за указанный интервал времени
    :param dates: кортеж, содержащий начало интервала времени и его окончание
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех продуктов, добавленных за указанный интервал времени
    """
    return await ProductFacade.get_models_by_date(
        dates=dates,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае объект ProductOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/{product_id}",
    response_model=ProductOutput,
    status_code=status.HTTP_200_OK,
)
async def get_product_by_id(
    product_id,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> ProductOutput:
    """
    Обрабатывает запрос с фронт энда на получение продукта по его id
    :param product_id: объект ProductOutput, который получается путем выполнения зависимости (метода product_by_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: ProductOutput
    """
    return ProductFacade.get_model_by_id(
        model_id=product_id,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае dict - {"status": "ok", "detail": "Product has been added"},
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post(
    "/",
    response_model=ProductOutput,
    status_code=status.HTTP_201_CREATED,
)
async def register_product(
    product_in: ProductInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> ProductOutput:
    """
    Обрабатывает запрос с фронт энда на добавление продукта в БД
    :param product_in: ProductInput - объект, содержащий данные продукта
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductFacade.register_model(
        scheme_in=product_in,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае dict - {"status": "ok", "detail": "Product has been updated"},
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put(
    "/{product_id}",
    response_model=ProductOutput,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_id: int,
    product_in: ProductInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> ProductOutput:
    """
    Обрабатывает запрос с фронт энда на полную замену данных продукта по его id
    :param product_in: ProductInput - объект, содержащий новые данные конкретного продукта
    :param product_id: Product_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductFacade.update_model(
        model_id=product_id,
        scheme_in=product_in,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае dict - {"status": "ok", "detail": "Product has been updated"},
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/{product_id}",
    response_model=ProductOutput,
    status_code=status.HTTP_200_OK,
)
async def update_product_partial(
    product_id: int,
    product_in: ProductInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> ProductOutput:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных продукта по его id
    :param product_in: ProductInput - объект, содержащий новые данные конкретного продукта
    :param product_id: Product_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductFacade.update_model(
        model_id=product_id,
        scheme_in=product_in,
        session=session,
        partial=True,
    )


@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_products(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductFacade.clear_table(session=session)


# response_model определяет модель ответа пользователю, в данном случае dict - {"status": "ok", "detail": "Product has been removing"},
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/{product_id}",
    response_model=ProductOutput,
    status_code=status.HTTP_200_OK,
)
async def del_product(
    product_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> ProductOutput:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного продукта
    :param product_id: Product_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductFacade.delete_model(
        model_id=product_id,
        session=session,
    )
