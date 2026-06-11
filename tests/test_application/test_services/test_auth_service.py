import time

import pytest


def test_register_success(auth_service, user_repository):
    username = 'user_a'
    email = 'user_a@anibase.com'
    password = '123123'

    created_user = auth_service.register_user(username, email, password)

    assert created_user is not None
    assert created_user.username == username
    assert created_user.email == email

    user_repository.delete(created_user.id)


def test_auth_success(auth_service, user_repository):
    test_time = int(time.time())
    username = f'user_a_{test_time}'
    email = f'user_a_{test_time}@anibase.com'
    password = 'qwerty123456'

    created_user = auth_service.register_user(username, email, password)
    token = auth_service.authenticate_user(email, password)

    assert token is not None

    user_repository.delete(created_user.id)


def test_auth_failure(auth_service, user_repository):
    test_time = int(time.time())
    username = f'user_a_{test_time}'
    email = f'user_a_{test_time}@anibase.com'
    password = 'qwerty123456'

    wrong_password = 'fasdfasdfasdfa'

    created_user = auth_service.register_user(username, email, password)
    with pytest.raises(ValueError):
        _ = auth_service.authenticate_user(email, wrong_password)

    user_repository.delete(created_user.id)