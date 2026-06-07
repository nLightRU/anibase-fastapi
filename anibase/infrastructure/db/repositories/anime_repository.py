from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from anibase.infrastructure.db.models import Anime


class AnimeRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, anime_id: UUID) -> type[AnimeRepository] | None:
        return self._session.get(AnimeRepository, anime_id)

    def get_by_tile(self, title: str) -> type[AnimeRepository] | None:
        return self._session.scalar(select(Anime).where(Anime.title == title))

    def list_all(self):
        return self._session.scalars(select(Anime)).all()

    def create(self, anime: Anime) -> Anime | None:
        self._session.add(anime)
        self._session.commit()
        self._session.refresh(anime)
        return anime

    def update(self, anime: Anime) -> Anime | None:
        self._session.merge(anime)
        self._session.commit()
        return anime

    def delete(self, anime: Anime):
        self._session.delete(anime)
        self._session.commit()