from uuid import UUID

from pydantic import BaseModel

from anibase.presentation.schemas.user import UserAnimeCreateRequest

class UserAnimeDTO(BaseModel):
    id: UUID
    user_id: UUID
    anime_id: UUID
    status: str
    score: int | None = None

    class Config:
        from_attributes = True

    @classmethod
    def from_request(cls, anime: UserAnimeCreateRequest, user_id: UUID) -> UserAnimeDTO:
        entry_id = UUID('00000000-0000-0000-0000-000000000000')
        return cls(
            id=entry_id,
            anime_id=anime.anime_id,
            user_id=user_id,
            status=anime.status,
            score=anime.score
        )
