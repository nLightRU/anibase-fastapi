from sqlalchemy import select

from anibase.application.dto import UserAnimeDTO
from anibase.infrastructure.db.models import User, Anime, UserAnime, UserAnimeStatus


def test_add_anime_to_user(
        db_session,
        anime_repository,
        roles,
        user_anime_repository
):
    user = User(
        username='test_user',
        email='test@example.com',
        password_hash='secret_hash_123',
        role_id = roles['user'].id
    )
    anime = Anime.create_test_anime()

    db_session.add(user)
    db_session.add(anime)
    db_session.commit()

    planning_status = db_session.scalar(
        select(UserAnimeStatus.name)
        .where(UserAnimeStatus.name == 'planning')
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