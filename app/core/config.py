
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parrent.parent


class DBSettings(BaseSettings):
    # Содержит в себе настройки и конфиги для подключения к БД

    # URL для подключения к базе # dialect+driver://username:password@host:port/database
    url: str = "postgresql+asyncpg://gsa:0502@localhost:8080/PostgreSQL"

    # Параметр, отвечающий за вывод логов в консоль при работе с БД
    echo: bool = True


db_settings = DBSettings()


class JWTSettings(BaseSettings):
    # Содержит в себе пути к публичному и приватному ключу, а так же алгоритм шифрования

    # Путь к приватному ключу
    private_key : Path = BASE_DIR / 'tokens' / 'jwt-private.pem'

    # Путь к публичному ключу
    public_key : Path = BASE_DIR / 'tokens' / 'jwt-public.pem'

    # Алгоритм шифрования
    algoritm: str = 'RS256'


jwt_settings = JWTSettings()
