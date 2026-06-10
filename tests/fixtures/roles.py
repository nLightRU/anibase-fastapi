import pytest
from sqlalchemy import select

from anibase.infrastructure.db.models import Role
from tests.fixtures.database import TestSessionLocal

@pytest.fixture(scope="session")
def roles_dict(setup_db) -> dict[str, Role]:
    session = TestSessionLocal()
    roles = session.scalars(select(Role))
    mapping = {}

    for r in roles:
        mapping[r.name] = r

    return mapping