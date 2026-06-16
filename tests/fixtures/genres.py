import pytest
from sqlalchemy import select

from anibase.infrastructure.db.models import Genre
from tests.fixtures.database import TestSessionLocal


@pytest.fixture(scope="session")
def genres_dict(setup_db) -> dict[str, Genre]:
    session = TestSessionLocal()
    genres = session.scalars(select(Genre))
    genres_dict = {genre.name: genre for genre in genres}
    session.close()
    return genres_dict
