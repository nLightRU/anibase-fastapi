import uuid

from pydantic import BaseModel, Field
from typing import Optional

from anibase.application.dto import AnimeDTO, GenreDTO
from anibase.application.enums import GenreEnum

class AnimeCreateRequest(BaseModel):
    title: str = Field(..., min_length=1,max_length=200)
    episodes: int = None
    rating: float = None
    description: Optional[str] = None
    is_hidden: bool = False
    genres: list[GenreEnum] = None

    def to_dto(self) -> AnimeDTO:
        anime_id = uuid.UUID('00000000-0000-0000-0000-000000000000')
        genres = [
            GenreDTO(id=uuid.UUID('00000000-0000-0000-0000-000000000000'), name=g)
            for g in self.genres
        ]
        return AnimeDTO(
            id=anime_id,
            title=self.title,
            description=self.description,
            episodes=self.episodes,
            is_hidden=self.is_hidden,
            genres=genres
        )

class AnimeResponse(BaseModel):
    id: uuid.UUID
    title: str = Field(..., min_length=1,max_length=200)
    episodes: int = None
    rating: float = None
    description: Optional[str] = None
    is_hidden: bool = False
    genres: list[GenreEnum] = None

    @classmethod
    def from_dto(cls, anime_dto: AnimeDTO):
        genres = [g.name for g in anime_dto.genres]
        return cls(
            id=anime_dto.id,
            title=anime_dto.title,
            episodes=anime_dto.episodes,
            is_hidden=anime_dto.is_hidden,
            genres=genres
        )


class AnimeUpdateRequest(BaseModel):
    id: uuid.UUID
    title: str = Field(None,min_length=1,max_length=200)
    description: Optional[str] = None
    episodes: int = None
    rating: float = None
    is_hidden: bool = None
    genres: list[GenreEnum] = None

    def to_dto(self) -> AnimeDTO:
        genres = [
            GenreDTO(id=uuid.UUID('00000000-0000-0000-0000-000000000000'), name=g)
            for g in self.genres
        ]
        return AnimeDTO(
            id=self.id,
            title=self.title,
            description=self.description,
            episodes=self.episodes,
            is_hidden=self.is_hidden,
            genres=genres
        )
