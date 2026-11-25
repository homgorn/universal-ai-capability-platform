"""Engine/session management. Postgres in production, SQLite for local/dev/tests."""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from uaicp.db.base import Base

DEFAULT_URL = "sqlite+pysqlite:///./uaicp.db"


def make_engine(url: str | None = None):
    resolved = url or os.getenv("DATABASE_URL") or DEFAULT_URL
    connect_args = {"check_same_thread": False} if resolved.startswith("sqlite") else {}
    return create_engine(resolved, future=True, connect_args=connect_args)


def make_session_factory(engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


engine = make_engine()
SessionLocal = make_session_factory(engine)


def init_db(target_engine=None) -> None:
    """Create all tables (dev/test convenience; production uses Alembic)."""
    Base.metadata.create_all(target_engine or engine)


@contextmanager
def session_scope(target_engine=None) -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    factory = make_session_factory(target_engine) if target_engine else SessionLocal
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()