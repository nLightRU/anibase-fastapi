import pytest

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

from anibase.infrastructure.db.models import (
    Base,
    Role,
    UserAnimeStatus,
    Genre,
)
from anibase.infrastructure.config import settings


test_engine = create_engine(settings.DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    try:
        if not session.scalar(select(Role)):
            session.add_all([
                Role(name='admin'),
                Role(name='moderator'),
                Role(name='user')
            ])
            session.commit()
        if not session.scalar(select(UserAnimeStatus)):
            session.add_all([
                UserAnimeStatus(name='planning'),
                UserAnimeStatus(name='watching'),
                UserAnimeStatus(name='completed'),
                UserAnimeStatus(name='on_hold'),
                UserAnimeStatus(name='dropped')
            ])
            session.commit()
        if not session.scalar(select(Genre)):
            session.add_all([
                Genre(name='Action'),
                Genre(name='Drama'),
                Genre(name='Comedy'),
                Genre(name='Fantasy'),
                Genre(name='Slice of Life'),
                Genre(name='Detective')
            ])
            session.commit()
    finally:
        session.close()
    yield


@pytest.fixture
def db_session():
    """Сессия для теста с автоматическим откатом."""
    session = TestSessionLocal()
    yield session
    session.rollback()
    session.close()
