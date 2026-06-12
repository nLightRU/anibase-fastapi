import time
import uuid

from sqlalchemy import select

from anibase.infrastructure.db.models import (
    Anime,
    User,
    UserAnime,
    UserAnimeStatus
)
from application.dto import UserAnimeDTO


def test_add_anime(db_session, roles_dict, user_anime_service):
    username = f'test_user_{int(time.time())}'
    email = f'{username}@anibase.com'

    test_anime = Anime.create_test_anime()
    test_user = User.create_test_user(
        email=email,
        username=username,
        role_id=roles_dict['user'].id
    )

    db_session.add_all([test_anime, test_user])
    db_session.commit()

    add_entry = UserAnimeDTO(
        id =uuid.uuid4(),
        anime_id=test_anime.id,
        user_id=test_user.id,
        score=8.0,
        status='planning'
    )

    entry = user_anime_service.add_anime_to_user(add_entry)
    assert entry is not None
    assert entry.anime_id == test_anime.id
    assert entry.user_id == test_user.id
    assert entry.status == 'planning'
    assert entry.score == 8.0

    e = db_session.get(UserAnime, entry.id)
    db_session.delete(e)
    db_session.delete(test_anime)
    db_session.delete(test_user)
    db_session.commit()


def test_remove_anime(db_session, roles_dict, user_anime_service):
    username = f'test_user_{int(time.time())}'
    email = f'{username}@anibase.com'
    test_anime = Anime.create_test_anime()
    test_user = User.create_test_user(username=username, email=email, role_id=roles_dict['user'].id)
    entry = UserAnime(
        anime_id=test_anime.id,
        user_id=test_user.id,
        status_id = db_session.scalar(
            select(UserAnimeStatus.id).where(UserAnimeStatus.name == 'planning')
        )
    )

    db_session.add_all([test_anime, test_user, entry])
    db_session.commit()

    user_anime_service.remove_anime_from_user(test_user.id, test_anime.id)

    entry = db_session.scalar(
        select(UserAnime)
        .where(UserAnime.id == test_user.id, UserAnime.anime_id == test_anime.id)
    )
    assert entry is None

    db_session.delete(test_anime)
    db_session.delete(test_user)
    db_session.commit()
