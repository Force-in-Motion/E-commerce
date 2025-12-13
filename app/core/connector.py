from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from . import db_settings
from typing import AsyncGenerator


class DBConnector:

    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Асинхронный генератор, который предоставляет сессию для FastAPI-маршрутов и автоматически закрывает её после использования.
        "Отдаёт" её маршруту (через yield), чтобы тот мог работать с базой.
        После завершения запроса закрывает сессию и возвращает ее в пул соединений
        :return:
        """
        async with self.session_factory() as session:
            yield session


db_connector = DBConnector(url=db_settings.url, echo=db_settings.echo)
