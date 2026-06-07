from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from anibase.infrastructure.db.models import UserAnime, UserAnimeStatus

class UserAnimeRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, entry_id: UUID) -> type[UserAnime] | None:
        return self._session.get(UserAnime, entry_id)

    def get_by_user_and_anime(self, user_id: UUID, anime_id: UUID) -> type[UserAnime] | None:
        return self._session.scalar(
            select(UserAnime)
            .where(UserAnime.user_id == user_id, UserAnime.anime_id == anime_id)
        )

    def list_by_user(self, user_id: UUID) -> list[type[UserAnime]] | None:
        return self._session.scalars(
            select(UserAnime)
            .where(UserAnime.user_id == user_id)
        ).all()

    def create(self, entry: UserAnime) -> UserAnime | None:
        self._session.add(entry)
        self._session.commit()
        self._session.refresh(entry)
        return entry

    def update(self, entry: UserAnime) -> UserAnime | None:
        self._session.merge(entry)
        self._session.commit()
        return entry


    def delete(self, entry: UserAnime):
        self._session.delete(entry)
        self._session.commit()


class UserAnimeStatusRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_name(self, name: str) -> type[UserAnimeStatus] | None:
        return self._session.scalar(select(UserAnimeStatus).where(UserAnimeStatus.name == name))