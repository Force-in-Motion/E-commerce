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


# def map_crud_errors_auto(func):
# Определяем функцию-декоратор, которая принимает один параметр func.

# func — это оригинальная функция или метод фасада, которую мы хотим обернуть.
# Параметр func нужен, чтобы мы могли вызвать его внутри декоратора и при необходимости перехватить исключения.

#  async def wrapper(cls, *args, **kwargs):
# Объявляем внутреннюю функцию-обёртку, которая заменит оригинальную функцию func.
#
# Параметры:
# cls — класс, так как мы используем декоратор на @classmethod.
# При вызове метода класса Python автоматически передаёт ссылку на сам класс как первый аргумент.
# *args — все позиционные аргументы метода (например, user_input, session).
# **kwargs — все именованные аргументы метода.

# Асинхронность (async) нужна, потому что методы фасада асинхронные (await используется внутри).

# try: return await func(cls, *args, **kwargs)
# Попытка вызвать исходный метод фасада с теми же аргументами, что были переданы.
# await нужен, потому что метод может быть асинхронным (например, обращение к базе через async SQLAlchemy).
# Если всё выполняется успешно, результат сразу возвращается, и никакой обработчик ошибок не нужен.

# except Exception as e:
# Ловим любое исключение, которое возникает при вызове исходной функции.
# Переменная e — экземпляр исключения, который поймали.
# Например, IntegrityError(), DatabaseError(), NotFoundError() и т.д.

# Мы используем Exception, чтобы поймать все ошибки и потом фильтровать их через словарь CRUD_TO_HTTP_MAP.

# adapter = getattr(cls, "adapter", None)
# getattr(object, name, default) — стандартная функция Python.
# Она пытается получить атрибут name у объекта object.
# В нашем случае:
# cls — класс фасада (UserFacade, OrderFacade и т.д.).
# "adapter" — атрибут фасада, который указывает на CRUD-класс (UserCrud).
# None — значение по умолчанию, если атрибут не найден.
# Это безопаснее, чем писать cls.adapter, потому что не будет выброшено AttributeError, если атрибута нет.

# model = getattr(adapter, "model", None)
# То же самое, что выше, но теперь берём модель из адаптера.
# Пример: если adapter = UserCrud, то adapter.model = User.
# Это нужно для формирования человеко-читаемого сообщения об ошибке, например "User already exists".
# Если adapter равен None, то и model тоже будет None.

# for exc_type, mapper in CRUD_TO_HTTP_MAP.items():
# CRUD_TO_HTTP_MAP — словарь вида:
# items() возвращает кортеж (ключ, значение) для каждой пары словаря.
# В нашем случае:
# exc_type — тип ошибки из CRUD (класс исключения, например IntegrityError)
# mapper — функция-лямбда, которая превращает эту ошибку в HTTPException.

# if isinstance(e, exc_type):
# Проверяем, является ли пойманное исключение e экземпляром класса exc_type.
# То есть, если e — это IntegrityError, то условие будет True.
# Позволяет выбрать правильный маппер для конкретного типа ошибки.

# raise mapper(e, model)
# Вызываем функцию-лямбду mapper, передаём в неё:
# e — сам пойманный экземпляр исключения
# model — класс модели (например, User)
# Лямбда возвращает объект HTTPException, который мы поднимаем (raise) — это финальная ошибка, которую увидит FastAPI.

# raise

# Если ни одно из условий isinstance не сработало (например, ошибка не в словаре CRUD_TO_HTTP_MAP), пробрасываем исключение дальше без изменения.
# Это важно, чтобы неожиданные ошибки не терялись.

# return wrapper
# Декоратор возвращает функцию-обёртку wrapper, которая теперь заменяет исходный метод фасада.
# Вызовы метода будут проходить через эту обёртку, перехватывая ошибки CRUD и автоматически превращая их в HTTPException.

# Ключевые моменты
# cls — класс фасада, нужен для обращения к атрибуту adapter.
# *args, **kwargs — все аргументы исходного метода, чтобы wrapper был универсальным.
# getattr(cls, "adapter", None) — безопасное получение атрибута, чтобы избежать AttributeError.
# for exc_type, mapper in CRUD_TO_HTTP_MAP.items(): — перебор всех известных ошибок CRUD, чтобы выбрать нужный способ трансформации.
# isinstance(e, exc_type) — проверка типа пойманной ошибки.
# raise mapper(e, model) — создаём и поднимаем соответствующий HTTPException.
