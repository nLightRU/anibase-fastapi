import pytest
from sqlalchemy import text

@pytest.mark.smoke
def test_db_connection(db_session):
    result = db_session.execute(text('SELECT 1'))
    assert result.scalar() == 1