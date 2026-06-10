import pytest
from sqlalchemy import select

from anibase.application.dto import UserAnimeDTO

from anibase.infrastructure.db.models import (
    User,
    Anime,
    UserAnime,
    UserAnimeStatus
)

from anibase.infrastructure.db.repositories.user_anime_repository import UserAnimeStatusEnum


@pytest.mark.parametrize('status', list(UserAnimeStatusEnum))
def test_add_anime_to_user(
        roles_dict,
        status,
        db_session,
        user_anime_repository
):
    user = User(
        username='test_user',
        email='test@example.com',
        password_hash='secret_hash_123',
        role_id = roles_dict['user'].id
    )
    anime = Anime.create_test_anime()

    db_session.add(user)
    db_session.add(anime)
    db_session.commit()

    planning_status = db_session.scalar(
        select(UserAnimeStatus.name)
        .where(UserAnimeStatus.name == status.value)
    )
    assert planning_status is not None

    entry = UserAnimeDTO(
        user_id=user.id,
        anime_id=anime.id,
        status=planning_status
    )
    created_entry = user_anime_repository.create(entry)

    assert created_entry is not None
    assert created_entry.anime_id == anime.id
    assert created_entry.user_id == user.id

    entry_model = db_session.scalar(
        select(UserAnime).
        where(
            UserAnime.anime_id == created_entry.anime_id,
            UserAnime.user_id == created_entry.user_id
        )
    )

    db_session.delete(entry_model)
    db_session.delete(user)
    db_session.delete(anime)
    db_session.commit()


def test_remove_anime_from_user(
        roles_dict,
        db_session,
        user_anime_repository
):
    role_id = roles_dict['user'].id
    test_user = User.create_test_user(role_id=role_id)
    test_anime = Anime.create_test_anime()
    status_id = db_session.scalar(
        select(UserAnimeStatus.id)
        .where(UserAnimeStatus.name == 'planning')
    )
    test_user_anime = UserAnime(
        user_id=test_user.id,
        anime_id=test_anime.id,
        status_id=status_id

    )

    db_session.add_all([
        test_user,
        test_anime,
    ])
    db_session.commit()

    db_session.add(test_user_anime)
    db_session.commit()
    db_session.refresh(test_user_anime)

    user_anime_repository.delete(test_user_anime.id)

    deleted_entry = db_session.scalar(
        select(UserAnime)
        .where(
            UserAnime.anime_id == test_anime.id,
            UserAnime.user_id == test_user.id
        )
    )

    assert deleted_entry is None

    db_session.delete(test_user)
    db_session.delete(test_anime)
    db_session.commit()
