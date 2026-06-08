import pytest

from sqlalchemy.exc import IntegrityError

from anibase.infrastructure.db.models import User
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
