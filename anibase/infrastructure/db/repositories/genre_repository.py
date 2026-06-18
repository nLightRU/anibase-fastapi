from sqlalchemy import select
from sqlalchemy.orm import Session

from anibase.application.dto import GenreDTO
from anibase.application.enums import GenreEnum
from anibase.infrastructure.db.models import Genre

class GenreRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, genre: str = None) -> GenreDTO:
        if genre not in GenreEnum:
            raise ValueError(f'Genre not found, chose from {[g.value for g in GenreEnum]}')
        existed = self._session.scalar(select(Genre).where(Genre.name == genre))
        if existed is not None:
            raise ValueError(f'Genre {genre} already exists')
        g = Genre(name=genre)
        self._session.add(g)
        self._session.commit()
        self._session.refresh(g)
        return GenreDTO(
            id=g.id,
            name=g.name
        )

    def list_genres(self) -> list[GenreDTO]:
        genres = self._session.scalars(select(Genre)).all()
        if genres:
            return [GenreDTO(id=g.id, name=g.name) for g in genres]
        return []


    def get_by_id(self, genre_id: UUID) -> GenreDTO | None:
        g = self._session.get(Genre, genre_id)
        if g is None:
            return None
        return g

    def update(self, genre_update: GenreDTO) -> GenreDTO:
        g = self._session.get(Genre, genre_update.id)
        if g is None:
            raise ValueError('Genre not found')
        g.name = genre_update.name
        self._session.commit()
        return GenreDTO(
            id=g.id,
            name=g.name
        )

    def delete(self, genre_id: UUID):
        g = self._session.get(Genre, genre_id)
        if g is None:
            raise ValueError('Genre not found')
        self._session.delete(g)
        self._session.commit()
