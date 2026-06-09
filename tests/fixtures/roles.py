import pytest

@pytest.fixture(scope="session")
def roles(setup_db, db_session):
    roles = db_session.scalars(select(Role))
    roles_dict = {}

    for r in roles:
        roles_dict[r.name] = r

    return roles_dict