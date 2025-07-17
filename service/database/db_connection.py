from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from asyncio import current_task

from settings import db_settings


class DBConnector:

    def __init__(self, url, echo):
        """При инициализации объекта, создает движок- create_async_engine и фабрику сессий - async_sessionmaker"""

        self.__engine = create_async_engine(  # Асинхронный движок, обязательным параметром ожидает url - путь к базе данных, в данном случае получаемый из db_settings
            url=url, echo=echo
        )

        self.__session_factory = async_sessionmaker(  # Фабрика сессий, ожидает:
            bind=self.__engine,  # движок
            autoflush=False,  # Отключает автоматическую отправку изменений в базу данных перед выполнением запросов
            autocommit=False,  # транзакции не завершаются автоматически.
            expire_on_commit=False,  # Отключает сброс (expiration) объектов в сессии после фиксации транзакции (commit).
        )

    def get_engine(self):
        """
        Возвращает асинхронный движок с указанными настройками
        :return: self.__engine
        """
        return self.__engine

    def __get_scoped_session(self):
        """
        Создаёт "scoped" сессию для работы с базой данных,
        Привязана к текущей задаче (task) в асинхронном приложении через scopefunc=current_task,
        session_factory=self.__session_factory: Указывает, какая фабрика будет создавать сессии (AsyncSession)
        scopefunc=current_task: Гарантирует, что каждая асинхронная задача (например, обработка HTTP-запроса в FastAPI) получает свою уникальную сессию
        :return:Объект async_scoped_session, который следит за тем, чтобы каждая задача использовала свою сессию, не мешая другим задачам
        """
        session = async_scoped_session(
            session_factory=self.__session_factory, scopefunc=current_task
        )

        return session

    async def session_dependency(self):
        """
        Асинхронный генератор, который предоставляет сессию для FastAPI-маршрутов и автоматически закрывает её после использования.
         Простыми словами: Он берёт сессию из __get_scoped_session.
        "Отдаёт" её маршруту (через yield), чтобы тот мог работать с базой.
        После завершения запроса закрывает сессию (await session.remove()) и возвращает ее в пул соединений
        :return:
        """
        session = self.__get_scoped_session()
        yield session
        await session.remove()


db_connector = DBConnector(url=db_settings.db_url, echo=db_settings.echo)


# Когда expire_on_commit=True (по умолчанию), SQLAlchemy помечает все объекты в сессии как "устаревшие" после commit,
# и их данные будут запрошены из базы при следующем обращении. Это может вызвать дополнительные запросы.

# С expire_on_commit=False объекты остаются в кэше сессии (Identity Map),
# и можно продолжать работать с ними без лишних запросов.
