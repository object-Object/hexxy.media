from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


# TODO: if we need other environment variables, refactor out model_config
class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="db_",
    )

    host: str
    port: int
    username: str = Field(alias="user")
    password: str = Field(alias="pass")
    database: str = Field(alias="name")

    @classmethod
    def model_validate_env(cls):
        return cls.model_validate({})

    @property
    def engine_url(self):
        """postgresql://user:pass@host:port/name"""
        return URL.create(
            drivername="postgresql",
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
        )
