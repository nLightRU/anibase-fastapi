from uuid import UUID

from anibase.application.dto import AnimeDTO
from anibase.infrastructure.db.repositories import AnimeRepository


class AnimeService:
    def __init__(self, anime_repository: AnimeRepository):
        self.anime_repository = anime_repository

    def create(self, anime: AnimeDTO) -> AnimeDTO:
        return self.anime_repository.create(anime)

    def get_by_id(self, anime_id: UUID) -> AnimeDTO:
        dto = self.anime_repository.get_by_id(anime_id)
        if dto is None:
            raise ValueError('Anime not found')
        return dto

    def list_anime(self) -> list[AnimeDTO]:
        return self.anime_repository.get_all()

    def update_anime(self, anime: AnimeDTO) -> AnimeDTO:
        return self.anime_repository.update(anime)

    def delete(self, anime_id: UUID):
        self.anime_repository.delete(anime_id)

