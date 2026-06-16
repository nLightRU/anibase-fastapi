import uuid

from pydantic import BaseModel, Field
from typing import Optional

from anibase.application.enums import GenreEnum

class AnimeCreateRequest(BaseModel):
    title: str = Field(..., min_length=1,max_length=200)
    episodes: int = None
    rating: float = None
    description: Optional[str] = None
    is_hidden: bool = False
    genres: list[GenreEnum] = None

class AnimeResponse(BaseModel):
    id: uuid.UUID
    title: str = Field(..., min_length=1,max_length=200)
    episodes: int = None
    rating: float = None
    description: Optional[str] = None
    is_hidden: bool = False
    genres: list[GenreEnum] = None


class AnimeUpdateRequest(BaseModel):
    id: uuid.UUID
    title: str = Field(None,min_length=1,max_length=200)
    description: Optional[str] = None
    episodes: int = None
    rating: float = None
    is_hidden: bool = None
