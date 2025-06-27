from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = 'postgresql+asyncpg://gsa:0502@db:5432/PostgreSQL'


settings = Settings()