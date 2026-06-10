from uuid import UUID

from pydantic import BaseModel

class UserAnimeDTO(BaseModel):
    user_id: UUID
    anime_id: UUID
    status: str
    score: int | None = None

    class Config:
        from_attributes = True