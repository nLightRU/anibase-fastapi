import time
from uuid import uuid4

import pytest

from anibase.application.dto import AnimeDTO, GenreDTO
from anibase.infrastructure.db.models import Anime


def test_create_no_genres(db_session, anime_repository):
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


def test_create_with_genre(db_session, genres_dict, anime_repository ):
    anime_title = f'Test Anime {int(time.time())}'
    anime_dto = AnimeDTO.create_test_anime(title=anime_title)
    genre = genres_dict['sports']
    anime_dto.genres.append(GenreDTO(id=genre.id, name=genre.name))
    created = anime_repository.create(anime_dto)

    anime_model: Anime = db_session.get(Anime, created.id)
    assert anime_model is not None
    assert genre.id == created.genres[0].id

    db_session.delete(anime_model)
    db_session.commit()

def test_create_with_two_genres(db_session, genres_dict, anime_repository ):
    anime_title = f'Test Anime {int(time.time())}'
    anime_dto = AnimeDTO.create_test_anime(title=anime_title)
    genres = [genres_dict['sports'], genres_dict['ecchi']]
    anime_dto.genres.extend(genres)
    created = anime_repository.create(anime_dto)

    assert created is not None
    assert len(created.genres) == 2


def test_get_by_id(db_session, genres_dict, anime_repository):
    test_model = Anime.create_test_anime()
    genres = [genres_dict['sports'], genres_dict['romance']]
    test_model.genres = genres

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
    assert len(test_dto.genres) == 2

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


def test_update_no_genre(db_session, anime_repository):
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


def test_update_with_genres(db_session, genres_dict, anime_repository):
    anime_title = f'Test Anime {int(time.time())}'
    test_genres = (genres_dict['sports'], genres_dict['romance'])
    test_model = Anime.create_test_anime(title=anime_title)
    test_model.genres.extend(test_genres)
    db_session.add(test_model)
    db_session.commit()

    update_data = AnimeDTO(
        id=test_model.id,
        title=anime_title,
        description=test_model.description,
        episodes=test_model.episodes,
        is_hidden=test_model.is_hidden,
        genres = [GenreDTO(id=test_genres[0].id, name=test_genres[0].name)]
    )
    updated = anime_repository.update(update_data)

    assert updated is not None
    assert len(updated.genres) == 1

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
