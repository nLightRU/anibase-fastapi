import pytest
from fastapi.testclient import TestClient
from anibase.main import app

pytest_plugins = [
    'tests.fixtures.database',
    'tests.fixtures.repositories'
]

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client