from uuid import UUID
from enum import Enum

from sqlalchemy import select
from sqlalchemy.orm import Session

from anibase.application.dto import UserAnimeDTO
from anibase.infrastructure.db.models import UserAnime, UserAnimeStatus


class UserAnimeStatusEnum(str, Enum):
    PLANNING = 'planning'
    WATCHING = 'watching'
    ON_HOLD = 'on_hold'
    COMPLETED = 'completed'
    DROPPED = 'dropped'

class UserAnimeRepository:
    def __init__(self, session: Session):
        self._session = session

    def _get_status_id(self, status: UserAnimeStatusEnum = None) -> UUID:
        if not isinstance(status, UserAnimeStatusEnum):
            raise ValueError(f"Invalid status. Choose from: {[e.value for e in UserAnimeStatusEnum]}")
        return self._session.scalar(
            select(UserAnimeStatus.id)
            .where(UserAnimeStatus.name == status.value)
        )

    @staticmethod
    def _create_dto(entry: UserAnime):
        return UserAnimeDTO(
            user_id=entry.user_id,
            anime_id=entry.anime_id,
            status=entry.status.name,
            score=entry.score
        )

    def create(self, entry: UserAnimeDTO) -> UserAnimeDTO | None:
        status_id = self._get_status_id(UserAnimeStatusEnum(value=entry.status))
        entry_model = UserAnime(
            user_id=entry.user_id,
            anime_id=entry.anime_id,
            status_id=status_id,
            score=entry.score
        )
        self._session.add(entry_model)
        self._session.commit()
        self._session.refresh(entry_model)
        return UserAnimeRepository._create_dto(entry_model)

    def get_by_id(self, entry_id: UUID) -> UserAnimeDTO | None:
        entry_model = self._session.get(UserAnime, entry_id)
        if not entry_model:
            return None
        return UserAnimeRepository._create_dto(entry_model)

    def get_by_user_and_anime(self, user_id: UUID, anime_id: UUID) -> UserAnimeDTO | None:
        entry_model = self._session.scalar(
            select(UserAnime)
            .where(UserAnime.user_id == user_id, UserAnime.anime_id == anime_id)
        )
        if not entry_model:
            return None
        return UserAnimeRepository._create_dto(entry_model)

    def list_by_user(self, user_id: UUID) -> list[UserAnimeDTO]:
        entries = self._session.scalars(
            select(UserAnime).where(UserAnime.user_id == user_id)
        )
        return [UserAnimeRepository._create_dto(e) for e in entries]

    def update(self, entry: UserAnimeDTO) -> UserAnimeDTO | None:
        entry_model = self._session.get(UserAnime, entry_id)
        if not entry_model:
            raise ValueError('Not found')

        entry_model.score = entry.score
        entry_model.status = entry.status
        self._session.commit()
        self._session.refresh(entry_model)

        return UserAnimeRepository._create_dto(entry_model)


    def delete(self, entry_id: UserAnime):
        entry_model = self._session.get(UserAnime, entry_id)
        if not entry_model:
            raise ValueError('Not found')

        self._session.delete(entry_model)
        self._session.commit()

class UserAnimeStatusRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_name(self, name: str) -> type[UserAnimeStatus] | None:
        return self._session.scalar(select(UserAnimeStatus).where(UserAnimeStatus.name == name))