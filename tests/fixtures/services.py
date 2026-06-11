import pytest

from application.services.anime_service import AnimeService
from application.services.auth_service import AuthService
from application.services.user_anime_service import UserAnimeService


@pytest.fixture
def auth_service(user_repository, role_repository):
    return AuthService(user_repository, role_repository)


@pytest.fixture
def anime_service(anime_repository):
    return AnimeService(anime_repository)


@pytest.fixture
def user_anime_service(user_anime_repository, anime_repository, user_repository):
    return UserAnimeService(user_anime_repository, anime_repository, user_repository)