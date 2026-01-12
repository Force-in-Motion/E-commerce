from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

PROJECT = Path(__file__).parent.parent.parent


class DBSettings(BaseSettings):
    """ Определяет настройки баз данных, которые считываются из .env файла """
    db_url: str

    echo: bool

    celery_broker_url: str

    celery_backend_url: str

    model_config = ConfigDict(env_file=".env", extra="ignore", env_prefix="DB_")


class SMTPSettings(BaseSettings):  
        """ Определяет настройки SMTP, которые считываются из .env файла """                          
        hostname: str

        port: int

        username: str

        password: str

        start_tls: bool

        model_config = ConfigDict(env_file=".env", extra="ignore", env_prefix="SMTP_")
        

class JWTSettings(BaseSettings):
    """ Определяет настройки JWT, которые считываются из .env файла """
    private_key: Path

    public_key: Path

    algorithm: str

    access_token_expire: int

    refresh_token_expire: int

    access_name: str

    refresh_name: str

    model_config = ConfigDict(env_file=".env", extra="ignore", env_prefix="JWT_")


db_settings = DBSettings()

jwt_settings = JWTSettings()
