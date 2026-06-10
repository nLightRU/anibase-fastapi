import pytest

from application.services.auth_service import AuthService


@pytest.fixture
def auth_service(user_repository, role_repository):
    return AuthService(user_repository, role_repository)