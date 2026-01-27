from app.repositories.cart import CartRepo
from app.schemas.cart import CartResponse
from app.service import BaseService
from datetime import datetime
from typing import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ProductRepo
from app.models import (
    Cart as Cart_model,
    CartProduct as Cart_Product_model,
)
from app.schemas import ProductAddOrUpdate, ProductInCart


class CartService(BaseService[CartRepo]):

    repo = CartRepo

    @classmethod
    def _to_cart_response(
        cls,
        cart_model: Cart_model,
    ) -> CartResponse:
        """
        Служебный метод, преобразует модель корзины и содержащиеся в ней продукты в Pydantic схему
        :param cart_model: ORM модель корзины
        :return: Pydantic схему корзины и содержащиеся в ней продукты
        """
        if cart_model is None:
            return None

        products = [
            ProductInCart(
                id=cp.product.id,
                name=cp.product.name,
                description=cp.product.description,
                price=cp.current_price,
                quantity=cp.quantity,
            )
            for cp in cart_model.products
        ]

        return CartResponse(
            id=cart_model.id,
            user_id=cart_model.user_id,
            products=products,
            created_at=cart_model.created_at,
            updated_at=cart_model.updated_at,
        )

    @classmethod
    async def get_all_carts(
        cls,
        session: AsyncSession,
        dates: tuple[datetime, datetime] = None,
    ) -> Optional[list[CartResponse]]:
        """
        Возвращает все корзины пользователей, содержащиеся в БД
        :param dates: Опциональный параметр, определяет временной диапазон
        :param session: Асинхронная сессия
        :return: возвращает все корзины и их продукты в виде Pydantic схем | None
        """
        if dates is not None:
            cart_models = await cls.repo.get_all_carts_by_date(
                dates=dates,
                session=session,
            )

        else:
            cart_models = await cls.repo.get_all_carts(session=session)

        if cart_models is None:
            return None

        return [cls._to_cart_response(cart) for cart in cart_models]

    @classmethod
    async def get_cart_model(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> Optional[Cart_model]:
        """
        Возвращает модель корзины согласно полученым параметрам
        :param session: Асинхронная сессия
        :param user_id: Опциональный параметр, id пользователя
        :param cart_id: Опциональный параметр, id  корзины
        :return: корзину виде Pydantic схемы | None
        """
        if user_id is not None:
            return await cls.repo.get_by_user_id(
                user_id=user_id,
                session=session,
            )

        if user_id is None:
            return await cls.repo.get_by_id(
                cart_id=cart_id,
                session=session,
            )

    @classmethod
    async def get_or_create_cart(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> CartResponse:
        """
        Возвращает модель корзины согласно полученым параметрам или создает и возвращает если она отсутствует
        :param session: Асинхронная сессия
        :param user_id: Опциональный параметр, id пользователя
        :param cart_id: Опциональный параметр, id  корзины
        :return: корзину виде Pydantic схемы
        """
        cart_model = await cls.get_cart_model(
            user_id=user_id,
            cart_id=cart_id,
            session=session,
        )

        if cart_model is None:
            cart_model = Cart_model(user_id=user_id)

            cart_model = await cls.repo.create(
                model=cart_model,
                session=session,
            )

        return cls._to_cart_response(cart_model)

    @classmethod
    async def add_or_update_product_in_cart(
        cls,
        session: AsyncSession,
        product_scheme: ProductAddOrUpdate,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> Optional[CartResponse]:
        """
        Добавляет продукт в корзину или изменяет его количество в ней
        :param session: Асинхронная сессия
        :param product_scheme: Pydantic схема - объект, содержащий данные о добавляемом продукте
        :param user_id: Опциональный параметр, id пользователя
        :param cart_id: Опциональный параметр, id  корзины
        :return: корзину виде Pydantic схемы | None
        """
        cart_model = await cls.get_cart_model(
            user_id=user_id,
            cart_id=cart_id,
            session=session,
        )

        if cart_model is None:
            return None

        product_in_cart = await cls.repo.get_product(
            session=session,
            cart_id=cart_model.id,
            product_id=product_scheme.product_id,
        )

        if not product_in_cart:
            product_model = await ProductRepo.get_by_id(
                model_id=product_scheme.product_id,
                session=session,
            )

            if product_model is None:
                return None

            product_in_cart = Cart_Product_model(
                cart_id=cart_model.id,
                quantity=product_scheme.quantity,
                product_id=product_model.id,
                current_price=product_model.price,
            )

            await cls.repo.create(
                model=product_in_cart,
                session=session,
            )

        else:
            new_data = {
                "product_id": product_scheme.product_id,
                "quantity": product_scheme.quantity,
            }

            await cls.repo.update(
                new_data=new_data,
                update_model=product_in_cart,
                session=session,
            )

        return await cls.get_or_create_cart(
            user_id=user_id,
            cart_id=cart_id,
            session=session,
        )

    @classmethod
    async def del_product_from_cart(
        cls,
        product_id: int,
        session: AsyncSession,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> Optional[CartResponse]:
        """
        Удаляет продукт из корзины
        :param session: Асинхронная сессия
        :param user_id: Опциональный параметр, id пользователя
        :param product_id: id продукта
        :param cart_id: Опциональный параметр, id  корзины
        :return: корзину виде Pydantic схемы | None
        """
        cart_model = await cls.get_cart_model(
            session=session,
            user_id=user_id,
            cart_id=cart_id,
        )

        if cart_model is None:
            return None

        product_in_cart = await cls.repo.get_product(
            session=session,
            cart_id=cart_model.id,
            product_id=product_id,
        )

        if product_in_cart is None:
            return None

        await cls.repo.delete(
            del_model=product_in_cart,
            session=session,
        )

        return await cls.get_or_create_cart(
            user_id=user_id,
            session=session,
        )

    @classmethod
    async def clear_user_cart(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> Optional[CartResponse]:
        """
        Очищает корзину от продуктов согласно полученым параметрам 
        :param session: объект асинхронной сессии
        :param user_id: Опциональный параметр, id пользователя
        :param cart_id: Опциональный параметр, id  корзины
        :return: Пустой список
        """

        cart_model = await cls.get_cart_model(
            session=session,
            user_id=user_id,
            cart_id=cart_id,
        )

        if cart_model is None:
            return None

        await cls.repo.clear_cart(
            session=session,
            cart_id=cart_model.id,
        )

        return await cls.get_or_create_cart(
            user_id=user_id,
            session=session,
        )
