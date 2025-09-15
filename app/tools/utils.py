from . import CRUD_TO_HTTP_MAP


class Utils:

    @staticmethod
    def map_crud_errors_auto(func):
        """
        Декоратор для фасада.
        Автоматически преобразует все ошибки CRUD в HTTPException.
        """

        async def wrapper(cls, *args, **kwargs):
            try:
                # Вызов исходного метода фасада
                return await func(cls, *args, **kwargs)
            except Exception as e:
                # Получаем адаптер и его модель
                adapter = getattr(cls, "adapter", None)
                model = getattr(adapter, "model", None)

                # Проходим по всем маппингам ошибок
                for exc_type, mapper in CRUD_TO_HTTP_MAP.items():
                    if isinstance(e, exc_type):
                        # Возвращаем HTTPException с нужным кодом и сообщением
                        raise mapper(e, model)

                # Если ошибка не в словаре — пробрасываем как есть
                raise

        return wrapper
