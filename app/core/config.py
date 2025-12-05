
from pydantic_settings import BaseSettings



class DBSettings(BaseSettings):
    # Содержит в себе настройки и конфиги для подключения к БД.
    # Все константы хранятся в файле .env, оттуда pydantic_settings их и возьмет при помощи класса Config

    # URL для подключения к базе # dialect+driver://username:password@host:port/database
    url: str

    # Параметр, отвечающий за вывод логов в консоль при работе с БД
    echo: bool

    class Config:
        env_file = '.env'

db_settings = DBSettings()


