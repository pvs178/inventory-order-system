from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


def get_engine():
    settings = get_settings()
    return create_engine(
        settings.database_url,
        echo=settings.echo_sql,
        pool_pre_ping=True,
    )


def get_session_factory():
    engine = get_engine()
    return sessionmaker(
        bind=engine,
        class_=Session,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
