from uuid import uuid4
import random

import pytest
from anibase.application.dto import GenreDTO
from anibase.infrastructure.db.models import Genre

test_genres_a = ('Action', 'Comedy', 'Slice of life')
test_genres_b = ('Drama', 'Detective', 'Fantasy')

def test_create(db_session, genre_repository):
    genre_str = random.choice(test_genres_a)
    genre = genre_repository.create(genre_str)
    assert genre is not None

    model = db_session.get(Genre, genre.id)
    assert model is not None
    assert model.id == genre.id
    assert model.name == genre.name

    db_session.delete(model)
    db_session.commit()


def test_get_by_id(db_session, genre_repository):
    genre_id = uuid4()
    genre_str = random.choice(test_genres_a)
    g = Genre(id=genre_id, name=genre_str)

    db_session.add(g)
    db_session.commit()

    test_dto = genre_repository.get_by_id(genre_id)

    assert test_dto is not None
    assert test_dto.id == genre_id
    assert test_dto.name == genre_str

    db_session.delete(g)
    db_session.commit()


def test_create_not_valid_name(db_session, genre_repository):
    genre_str = 'Abcde'
    with pytest.raises(ValueError):
        genre = genre_repository.create(genre_str)


def test_get_by_name(db_session, genre_repository):
    ...


def test_update(db_session, genre_repository):
    genre_str = random.choice(test_genres_a)
    g = Genre(id=uuid4(), name=genre_str)

    db_session.add(g)
    db_session.commit()
    db_session.refresh(g)

    update_dto = GenreDTO(id=g.id, name=random.choice(test_genres_b))
    updated = genre_repository.update(update_dto)

    assert updated is not None
    assert updated.id == update_dto.id
    assert updated.name == update_dto.name

    db_session.delete(g)
    db_session.commit()


def test_delete(db_session, genre_repository):
    genre_id = uuid4()
    g = Genre(id=genre_id, name=random.choice(test_genres_a))
    db_session.add(g)
    db_session.commit()

    genre_repository.delete(genre_id)

    deleted = db_session.get(Genre, genre_id)

    assert deleted is None

