import pytest

from sqlalchemy.exc import IntegrityError

from anibase.infrastructure.db.models import (
    User, Anime, UserAnime, UserAnimeStatus
)
from anibase.infrastructure.db.repositories import (
    UserRepository, RoleRepository
)

def test_get_role(db_session):
    role_repo = RoleRepository(db_session)
    role = role_repo.get_by_name('user')
    assert role is not None


def test_create_user(db_session, user_repository, role_repository):
    role = role_repository.get_by_name('user')
    test_user = User(
        username='test_user',
        email='test@example.com',
        password_hash='secret_hash_123',
        role_id=role.id
    )
    created_user = user_repository.create(test_user)
    assert created_user.id is not None
    assert created_user.username == 'test_user'


def test_get_by_email(db_session, user_repository, role_repository):
    role = role_repository.get_by_name('user')
    test_user = User(
        username='test_user',
        email='test@example.com',
        password_hash='secret_hash_123',
        role_id=role.id
    )
    db_session.add(test_user)
    db_session.commit()

    fetched_user = user_repository.get_by_email('test@example.com')

    assert fetched_user is not None
    assert fetched_user.username == 'test_user'
    assert fetched_user.email == 'test@example.com'


def test_email_unique(db_session, user_repository, role_repository):
    role = role_repository.get_by_name('user')
    test_user_a = User(
        username='test_user_a',
        email='test@example.com',
        password_hash='password_hash_123',
        role_id=role.id
    )

    user_repository.create(test_user_a)

    test_user_b = User(
        username='test_user_b',
        email='test@example.com',
        password_hash='password_hash_123',
        role_id=role.id
    )

    with pytest.raises(IntegrityError):
        user_repository.create(test_user_b)


def test_create_anime(db_session, anime_repository):
    bleach = Anime(
        title='Bleach',
        episodes=222,
        is_hidden=False
    )
    created = anime_repository.create(bleach)

    assert created is not None
    assert created.title == 'Bleach'
    assert created.episodes == 222


def test_list_anime(db_session, anime_repository):
    bleach = Anime(
        title='Bleach',
        episodes=222,
        is_hidden=False
    )

    one_piece = Anime(
        title='One Piece',
        episodes=1234,
        is_hidden=False
    )

    anime_repository.create(bleach)
    anime_repository.create(one_piece)

    anime = anime_repository.list_all()
    assert anime is not None
    assert isinstance(anime, list)
    assert len(anime) == 2


def test_add_anime_to_user(
        db_session,
        anime_repository,
        role_repository,
        user_repository,
        user_anime_status_repository,
        user_anime_repository
):
    role = role_repository.get_by_name('user')
    user = User(
        username='test_user',
        email='test@example.com',
        password_hash='secret_hash_123',
        role_id = role.id
    )
    created_user = user_repository.create(user)

    anime = Anime(
        title='Bleach',
        episodes=222,
        is_hidden=False
    )
    created_anime = anime_repository.create(anime)
    planning_status = user_anime_status_repository.get_by_name('planning')

    entry = UserAnime(
        user_id=created_user.id,
        anime_id=created_anime.id,
        status_id=planning_status.id
    )
    created_entry = user_anime_repository.create(entry)

    assert created_entry is not None
    assert created_entry.anime_id == created_anime.id
    assert created_entry.user_id == created_user.id

    # user_anime_repository.delete(entry)
    # anime_repository.delete(created_anime)
    # user_repository.delete(created_user)
