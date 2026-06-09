import pytest
from sqlalchemy import select

from anibase.infrastructure.db.models import Role
from tests.fixtures.database import TestSessionLocal

@pytest.fixture(scope="session")
def roles(setup_db) -> dict[str, Role]:
    session = TestSessionLocal()
    roles = session.scalars(select(Role))
    roles_dict = {}

    for r in roles:
        roles_dict[r.name] = r

    return roles_dict