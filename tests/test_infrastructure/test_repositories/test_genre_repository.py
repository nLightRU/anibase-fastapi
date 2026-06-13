import random

from anibase.infrastructure.db.models import Genre

def test_create(db_session, genre_repository):
    genre_str = random.choice(
        ('Action', 'Comedy', 'Slice of life', 'Drama', 'Detective')
    )
    genre = genre_repository.create(genre_str)
    assert genre is not None

    model = db_session.get(Genre, genre.id)
    assert model is not None
    assert model.id == genre.id
    assert model.name == genre.name

    db_session.delete(model)
    db_session.commit()