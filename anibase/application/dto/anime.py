from uuid import UUID

from pydantic import BaseModel

class AnimeDTO(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    episodes: int
    is_hidden: bool

    class Config:
        from_attributes = True
