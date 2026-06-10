from uuid import uuid4

import pytest

from anibase.application.dto import UserDTO
from anibase.infrastructure.db.models import User


def test_create(db_session, user_repository):
    user_dto = UserDTO(
        id = uuid4(),
        email='test_user@example.com',
        username='test_user',
        password_hash='secret123',
        role='user'
    )

    user_repository.create(user_dto)
    user_model = db_session.get(User, user_dto.id)

    assert user_model is not None
    assert user_model.email == user_dto.email
    assert user_model.username == user_dto.username
    assert user_model.password_hash == user_dto.password_hash
    assert user_model.role.name == user_dto.role

    db_session.delete(user_model)
    db_session.commit()


def test_get_by_id(db_session, user_repository, roles_dict):
    role = roles_dict['user']

    user_model = User(
        username='test_user',
        email='test_user@example.com',
        password_hash='secret123',
        role_id = role.id
    )
    db_session.add(user_model)
    db_session.commit()
    db_session.refresh(user_model)

    user_dto = user_repository.get_by_id(user_model.id)
    assert user_dto is not None
    assert user_dto.email == user_model.email
    assert user_dto.username == user_model.username
    assert user_dto.password_hash == user_model.password_hash
    assert user_dto.role == user_model.role.name

    db_session.delete(user_model)
    db_session.commit()


def test_get_by_id_none(db_session, user_repository, roles_dict):
    role = roles_dict['user']
    user_id = uuid4()
    not_found_id = uuid4()

    user_model = User(
        id=user_id,
        username='test_user',
        email='test@example.com',
        password_hash='12312asdf',
        role_id = role.id
    )

    db_session.add(user_model)
    db_session.commit()

    user_dto = user_repository.get_by_id(not_found_id)
    assert user_dto is None

    db_session.delete(user_model)
    db_session.commit()


def test_get_by_email(db_session, user_repository, roles_dict):
    role = roles_dict['user']

    user_model = User(
        username='test_user',
        email='test_user@example.com',
        password_hash='secret123',
        role_id=role.id
    )
    db_session.add(user_model)
    db_session.commit()
    db_session.refresh(user_model)

    user_dto = user_repository.get_by_email(user_model.email)
    assert user_dto is not None
    assert user_dto.email == user_model.email
    assert user_dto.username == user_model.username
    assert user_dto.password_hash == user_model.password_hash
    assert user_dto.role == user_model.role.name

    db_session.delete(user_model)
    db_session.commit()


def test_get_list(db_session, user_repository, roles_dict):
    role = roles_dict['user']

    user_model_a = User(
        username='test_user_a',
        email='test_user_a@example.com',
        password_hash='secret123',
        role_id=role.id
    )

    user_model_b = User(
        username='test_user',
        email='test_user_b@example.com',
        password_hash='secret123',
        role_id=role.id
    )

    db_session.add_all([user_model_a, user_model_b])
    db_session.commit()
    db_session.refresh(user_model_a)
    db_session.refresh(user_model_b)

    users = user_repository.get_all()
    assert len(users) == 2

    db_session.delete(user_model_a)
    db_session.delete(user_model_b)
    db_session.commit()


def test_update(db_session, user_repository, roles_dict):
    role = roles_dict['user']
    user_id = uuid4()

    user_model = User(
        id=user_id,
        username='test_user_a',
        email='test_user_a@example.com',
        password_hash='secret123',
        role_id=role.id
    )

    user_dto = UserDTO(
        id=user_id,
        username='test_b',
        email='test_b@example.com',
        password_hash='secret123',
        role=role.name
    )

    db_session.add(user_model)
    db_session.commit()

    user_updated = user_repository.update(user_dto)

    assert user_updated.username == user_dto.username
    assert user_updated.email == user_dto.email
    assert user_updated.password_hash == user_dto.password_hash
    assert user_updated.role == user_dto.role

    db_session.delete(user_model)
    db_session.commit()


def test_update_not_found(db_session, user_repository, roles_dict):
    user_id = uuid4()
    not_found_id = uuid4()
    user_model = User(
        id = user_id,
        username='test_user',
        email='test@example.com',
        password_hash='secret123',
        role_id=roles_dict['user'].id
    )

    db_session.add(user_model)
    db_session.commit()

    user_dto = UserDTO(
        id=not_found_id,
        username='test_user',
        email='test@ex.com',
        password_hash='fasdfasdfasdf',
        role = roles_dict['user'].name
    )

    with pytest.raises(ValueError):
        user_repository.update(user_dto)

    db_session.delete(user_model)
    db_session.commit()


def test_delete(db_session, user_repository, roles_dict):
    role = roles_dict['user']
    user_id = uuid4()

    user_model = User(
        id=user_id,
        username='test_user_a',
        email='test_user_a@example.com',
        password_hash='secret123',
        role_id=role.id
    )

    db_session.add(user_model)
    db_session.commit()

    user_repository.delete(user_id)

    deleted_user = db_session.get(User, user_id)

    assert deleted_user is None
