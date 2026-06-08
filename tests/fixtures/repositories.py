import pytest

from anibase.infrastructure.db.repositories import (
    AnimeRepository,
    UserRepository,
    UserAnimeRepository,
    UserAnimeStatusRepository,
    RoleRepository
)


@pytest.fixture
def anime_repository(db_session):
    return AnimeRepository(session=db_session)


@pytest.fixture
def user_repository(db_session):
    return UserRepository(session=db_session)


@pytest.fixture
def user_anime_repository(db_session):
    return UserAnimeRepository(session=db_session)


@pytest.fixture
def user_anime_status_repository(db_session):
    return UserAnimeStatusRepository(session=db_session)


@pytest.fixture
def role_repository(db_session):
    return RoleRepository(session=db_session)