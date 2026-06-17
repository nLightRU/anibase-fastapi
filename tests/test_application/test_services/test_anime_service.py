import time

import pytest

from anibase.infrastructure.db.models import Anime
from anibase.application.dto import AnimeDTO

def test_create_anime_no_genres(db_session, anime_service):
    title = f'Test Anime {int(time.time())}'
    test_dto = AnimeDTO.create_test_anime(title=title)
    created_dto = anime_service.create_anime(test_dto)
    assert isinstance(created_dto, AnimeDTO)
    assert created_dto.id == test_dto.id
    assert created_dto.title == test_dto.title
    assert created_dto.description == test_dto.description
    assert created_dto.episodes == test_dto.episodes
    assert created_dto.is_hidden == test_dto.is_hidden

    model = db_session.get(Anime, test_dto.id)
    db_session.delete(model)
    db_session.commit()


def test_get_anime_no_genres(db_session, anime_service):
    title = f'Test Anime {int(time.time())}'
    test_model = Anime.create_test_anime(title=title)
    db_session.add(test_model)
    db_session.commit()

    anime_dto = anime_service.get_anime_by_id(test_model.id)
    assert isinstance(anime_dto, AnimeDTO)
    assert anime_dto.id == test_model.id
    assert anime_dto.title == test_model.title
    assert anime_dto.description == test_model.description
    assert anime_dto.episodes == test_model.episodes
    assert anime_dto.is_hidden == test_model.is_hidden

    db_session.delete(test_model)
    db_session.commit()


def test_update_anime_no_genres(db_session, anime_service):
    title = f'Test Anime {int(time.time())}'
    test_model = Anime.create_test_anime(title=title)

    db_session.add(test_model)
    db_session.commit()

    updated_title = test_model.title + 'TEST UPDATE'
    updated_description = test_model.description + 'TEST UPDATE'
    updated_episodes=1234
    updated_is_hidden=not test_model.is_hidden

    update_data = AnimeDTO(
        id=test_model.id,
        title=updated_title,
        description=updated_description,
        episodes=updated_episodes,
        is_hidden=updated_is_hidden,
        genres=None
    )

    updated_dto = anime_service.update_anime(update_data)
    assert isinstance(updated_dto, AnimeDTO)
    assert updated_dto.id == test_model.id
    assert updated_dto.title == updated_title
    assert updated_dto.description == updated_description
    assert updated_dto.episodes == updated_episodes
    assert updated_dto.is_hidden == updated_is_hidden

    db_session.delete(test_model)
    db_session.commit()


def test_delete_anime(db_session, anime_service):
    test_model = Anime.create_test_anime(title='Test Anime Delete')
    db_session.add(test_model)
    db_session.commit()

    anime_service.delete(test_model.id)
