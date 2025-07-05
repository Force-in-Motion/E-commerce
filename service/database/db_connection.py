from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session)
from asyncio import current_task

from settings import db_settings




class DBConnector:
    def __init__(self, url, echo):
        self.__engine = create_async_engine(url=url, echo=echo)
        self.__session_factory = async_sessionmaker(
            bind=self.__engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False)


    def get_engine(self):
        """
        Возвращает асинхронный движок с указанными настройками
        :return: self.__engine
        """
        return self.__engine


    def __get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.__session_factory,
            scopefunc=current_task
        )

        return session


    async def session_dependency(self):
        session = self.__get_scoped_session()
        yield session
        await session.remove()



db_connector = DBConnector(db_settings.db_url, db_settings.echo)