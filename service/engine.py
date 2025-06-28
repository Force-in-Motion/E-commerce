from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings.db_config import settings




class Engine:
    def __init__(self, url, echo):
        self.__engine = create_async_engine(url=url, echo=echo)
        self.__session_factory = async_sessionmaker(bind=self.__engine, autoflush=False, autocommit=False, expire_on_commit=False)


    def get_engine(self):
        return self.__engine


    def get_session_factory(self):
        return self.__session_factory



engine = Engine(settings.db_url, settings.echo)