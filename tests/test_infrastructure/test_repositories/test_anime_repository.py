from uuid import uuid4

import pytest

from anibase.application.dto import AnimeDTO
from anibase.infrastructure.db.models import Anime


def test_create(db_session, anime_repository):
    anime_dto = AnimeDTO.create_test_anime()

    anime_repository.create(anime_dto)
    anime_model = db_session.get(Anime, anime_dto.id)

    assert anime_model is not None
    assert anime_model.id == anime_dto.id
    assert anime_model.title == anime_dto.title
    assert anime_model.description == anime_dto.description
    assert anime_model.episodes == anime_dto.episodes
    assert anime_model.is_hidden == anime_dto.is_hidden

    db_session.delete(anime_model)
    db_session.commit()


def test_get_by_id(db_session, anime_repository):
    test_model = Anime.create_test_anime()

    db_session.add(test_model)
    db_session.commit()
    db_session.refresh(test_model)

    test_dto = anime_repository.get_by_id(test_model.id)
    assert test_dto is not None
    assert test_dto.id == test_model.id
    assert test_dto.title == test_model.title
    assert test_dto.description == test_model.description
    assert test_dto.episodes == test_model.episodes
    assert test_dto.is_hidden == test_model.is_hidden

    db_session.delete(test_model)
    db_session.commit()


def test_get_by_id_none(db_session, anime_repository):
    anime_id = uuid4()
    not_found_id = uuid4()

    test_model = Anime.create_test_anime(anime_id=anime_id)

    db_session.add(test_model)
    db_session.commit()

    test_dto = anime_repository.get_by_id(not_found_id)
    assert test_dto is None

    db_session.delete(test_model)
    db_session.commit()


def test_get_list(db_session, anime_repository):
    test_model_a = Anime.create_test_anime(title='Test Anime A')
    test_model_b = Anime.create_test_anime(title='Test Anime B')

    db_session.add_all([test_model_a, test_model_b])
    db_session.commit()
    db_session.refresh(test_model_a)
    db_session.refresh(test_model_b)

    anime = anime_repository.get_all()
    assert len(anime) > 0
    assert isinstance(anime, list)

    db_session.delete(test_model_a)
    db_session.delete(test_model_b)
    db_session.commit()


def test_update(db_session, anime_repository):
    anime_id = uuid4()

    test_model = Anime.create_test_anime(
        anime_id=anime_id,
        title='Test Anime 123',
        description='Test Anime description',
        episodes=12,
        is_hidden=False
    )

    test_dto = AnimeDTO.create_test_anime(
        anime_id=anime_id,
        title='Test Anime 456',
        description='Test Anime description 456',
        episodes=16,
        is_hidden=True
    )

    db_session.add(test_model)
    db_session.commit()

    anime_updated = anime_repository.update(test_dto)

    assert anime_updated is not None
    assert anime_updated.id == anime_id
    assert anime_updated.title == test_dto.title
    assert anime_updated.description == test_dto.description
    assert anime_updated.episodes == test_dto.episodes
    assert anime_updated.is_hidden == test_dto.is_hidden

    db_session.delete(test_model)
    db_session.commit()


def test_delete(db_session, anime_repository):
    anime_id = uuid4()
    test_model = Anime.create_test_anime(anime_id=anime_id)
    db_session.add(test_model)
    db_session.commit()

    anime_repository.delete(anime_id)
    deleted_anime = db_session.get(Anime, anime_id)

    assert deleted_anime is None
