import pytest

from anibase.infrastructure.db.models import Anime
from anibase.application.dto import AnimeDTO

def test_create_anime(db_session, random_anime_dto, anime_service):
    created_anime = anime_service.create(random_anime_dto)
    assert isinstance(created_anime, AnimeDTO)
    assert created_anime.id == random_anime_dto.id
    assert created_anime.title == random_anime_dto.title
    assert created_anime.description == random_anime_dto.description
    assert created_anime.episodes == random_anime_dto.episodes
    assert created_anime.is_hidden == random_anime_dto.is_hidden

    anime_model = db_session.get(Anime, random_anime_dto.id)
    db_session.delete(anime_model)
    db_session.commit()


def test_get_anime(db_session, random_anime, anime_service):
    db_session.add(random_anime)
    db_session.commit()

    anime_dto = anime_service.get_by_id(random_anime.id)
    assert isinstance(anime_dto, AnimeDTO)
    assert anime_dto.id == random_anime.id
    assert anime_dto.title == random_anime.title
    assert anime_dto.description == random_anime.description
    assert anime_dto.episodes == random_anime.episodes
    assert anime_dto.is_hidden == random_anime.is_hidden


def test_update_anime(db_session, random_anime, anime_service):
    db_session.add(random_anime)
    db_session.commit()

    updated_title = random_anime.title + 'TEST UPDATE'
    updated_description = random_anime.description + 'TEST UPDATE'
    updated_episodes=1234
    updated_is_hidden=not random_anime.is_hidden

    update_data = AnimeDTO(
        id=random_anime.id,
        title=updated_title,
        description=updated_description,
        episodes=updated_episodes,
        is_hidden=updated_is_hidden
    )

    updated_dto = anime_service.update_anime(update_data)
    assert isinstance(updated_dto, AnimeDTO)
    assert updated_dto.id == random_anime.id
    assert updated_dto.title == updated_title
    assert updated_dto.description == updated_description
    assert updated_dto.episodes == updated_episodes
    assert updated_dto.is_hidden == updated_is_hidden

    db_session.delete(random_anime)
    db_session.commit()


def test_delete_anime(db_session, random_anime, anime_service):
    db_session.add(random_anime)
    db_session.commit()

    anime_service.delete(random_anime.id)

