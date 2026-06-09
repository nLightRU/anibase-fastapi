from uuid import UUID, uuid4

from pydantic import BaseModel

class AnimeDTO(BaseModel):
    id: UUID
    title: str
    description: str | None
    episodes: int
    is_hidden: bool

    class Config:
        from_attributes = True

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
            is_hidden=is_hidden
        )
