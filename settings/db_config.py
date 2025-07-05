from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    db_url: str = 'postgresql+asyncpg://gsa:0502@localhost:8080/PostgreSQL'
    echo: bool = True

db_settings = DBSettings()