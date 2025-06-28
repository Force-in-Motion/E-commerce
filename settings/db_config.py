from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = 'postgresql+asyncpg://gsa:0502@localhost:8080/PostgreSQL'
    echo: bool = True

settings = Settings()