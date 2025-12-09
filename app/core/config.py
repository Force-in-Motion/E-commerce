from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

PROJECT = Path(__file__).parent.parent.parent


class DBSettings(BaseSettings):

    url: str

    echo: bool

    model_config = ConfigDict(env_file=".env", extra="ignore", env_prefix="DB_")


class JWTSettings(BaseSettings):

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
