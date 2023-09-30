from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


# TODO: if we need other environment variables, refactor out model_config
class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    @classmethod
    def model_validate_env(cls):
        return cls.model_validate({})

    @property
    def engine_url(self):
        """postgresql://user:pass@host:port/name"""
        return URL.create(
            drivername="postgresql",
            host=self.db_host,
            port=self.db_port,
            username=self.db_user,
            password=self.db_pass,
            database=self.db_name,
        )
