from uuid import UUID

from pydantic import BaseModel

class UserAnimeDTO(BaseModel):
    user_id: UUID
    anime_id: UUID
    status: str
    score: Optional[int]

    class Config:
        from_attributes = True