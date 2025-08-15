from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    # Содержит в себе настройки и конфиги для подключения к БД

    # URL для подключения к базе # dialect+driver://username:password@host:port/database
    url: str = "postgresql+asyncpg://gsa:0502@localhost:8080/PostgreSQL"

    # Параметр, отвечающий за вывод логов в консоль при работе с БД
    echo: bool = True


db_settings = DBSettings()
