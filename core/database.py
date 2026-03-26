from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from aurora_tms_mvp import Base, engine, SessionLocal

__all__ = ["Base", "engine", "SessionLocal"]

SQLALCHEMY_DATABASE_URL = "sqlite:///./aurora_tms.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()