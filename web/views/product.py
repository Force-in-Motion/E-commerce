from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.database.crud import ProductAdapter
from service.database import db_connector
from service.database.models import Product as Product_model
from web.schemas import ProductInput, ProductOutput
from tools import product_by_id


router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов ProductOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get("/", response_model=list[ProductOutput], status_code=status.HTTP_200_OK)
async def get_products(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[ProductOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех продуктов
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: list[ProductOutput]
    """
    return await ProductAdapter.get_products(session)


# response_model определяет модель ответа пользователю, в данном случае объект ProductOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get("/{id}", response_model=ProductOutput, status_code=status.HTTP_200_OK)
async def get_product_by_id(
    product: ProductOutput = Depends(product_by_id),
) -> ProductOutput:
    """
    Обрабатывает запрос с фронт энда на получение продукта по его id
    :param product: объект ProductOutput, который получается путем выполнения зависимости (метода product_by_id)
    :return: ProductOutput
    """
    return product


# response_model определяет модель ответа пользователю, в данном случае dict - {"status": "ok", "detail": "Product has been added"},
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_product(
    product: ProductInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict:
    """
    Обрабатывает запрос с фронт энда на добавление продукта в БД
    :param product: ProductInput - объект, содержащий данные продукта
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductAdapter.add_product(product, session)


# response_model определяет модель ответа пользователю, в данном случае dict - {"status": "ok", "detail": "Product has been updated"},
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_product(
    product_input: ProductInput,
    product_model: Product_model = Depends(product_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict:
    """
    Обрабатывает запрос с фронт энда на полную замену данных продукта по его id
    :param product_input: ProductInput - объект, содержащий новые данные конкретного продукта
    :param product_model: Product_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductAdapter.update_product(product_input, product_model, session)


# response_model определяет модель ответа пользователю, в данном случае dict - {"status": "ok", "detail": "Product has been updated"},
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_product_partial(
    product_input: ProductInput,
    product_model: Product_model = Depends(product_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных продукта по его id
    :param product_input: ProductInput - объект, содержащий новые данные конкретного продукта
    :param product_model: Product_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductAdapter.update_product(
        product_input, product_model, session, partial=True
    )


@router.delete("/clear", response_model=dict, status_code=status.HTTP_200_OK)
async def clear_products(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на удаление всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductAdapter.clear_product_db(session)


# response_model определяет модель ответа пользователю, в данном случае dict - {"status": "ok", "detail": "Product has been removing"},
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def del_product(
    product_model: Product_model = Depends(product_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного продукта
    :param product_model: Product_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await pa.del_product(product_model, session)
