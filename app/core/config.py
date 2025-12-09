
from pydantic_settings import BaseSettings



class DBSettings(BaseSettings):
    """Содержит в себе настройки и конфиги для подключения к БД"""

    url: str

    echo: bool

    class Config:
        env_file = '.env'

db_settings = DBSettings()


