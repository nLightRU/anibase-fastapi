import pytest

from application.services.anime_service import AnimeService
from application.services.auth_service import AuthService


@pytest.fixture
def auth_service(user_repository, role_repository):
    return AuthService(user_repository, role_repository)


@pytest.fixture
def anime_service(anime_repository):
    return AnimeService(anime_repository)