from sqlmodel import Session, create_engine

from .settings import DBSettings

_settings = DBSettings.model_validate_env()
_engine = create_engine(_settings.engine_url)


def check_connection():
    with Session(_engine) as session:
        session.connection()


def get_session():
    with Session(_engine) as session:
        yield session
