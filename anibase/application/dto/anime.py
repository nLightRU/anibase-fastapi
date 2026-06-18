from uuid import UUID, uuid4

from pydantic import BaseModel

from anibase.presentation.schemas.anime import AnimeCreateRequest
from anibase.presentation.schemas.anime import AnimeUpdateRequest
from anibase.application.dto.genre import GenreDTO


class AnimeDTO(BaseModel):
    id: UUID
    title: str
    description: str | None
    episodes: int
    is_hidden: bool
    genres: list[GenreDTO] | None

    class Config:
        from_attributes = True

    @classmethod
    def from_request_scheme(cls, body: AnimeCreateRequest | AnimeUpdateRequest) -> AnimeDTO:
        anime_id = UUID('00000000-0000-0000-0000-000000000000')
        if isinstance(body, AnimeUpdateRequest):
            anime_id = body.id
        genres = [
            GenreDTO( id=UUID('00000000-0000-0000-0000-000000000000'), name=g)
            for g in body.genres
        ]
        return cls(
            id=anime_id,
            title=body.title,
            description=body.description,
            episodes=body.episodes,
            is_hidden=body.is_hidden,
            genres=genres
        )

    @classmethod
    def create_test_anime(
        cls,
        anime_id: UUID = None, title: str = 'Test Anime',
        description: str = 'Test Anime description', episodes: int = 10,
        is_hidden: bool = False
    ):
        if not anime_id:
            anime_id = uuid4()
        return cls(
            id=anime_id, title=title,
            description=description, episodes=episodes,
            is_hidden=is_hidden,
            genres=[]
        )
