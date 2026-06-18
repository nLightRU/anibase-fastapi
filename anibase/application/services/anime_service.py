from uuid import UUID, uuid4

from anibase.application.enums import GenreEnum
from anibase.application.dto import AnimeDTO, GenreDTO
from anibase.infrastructure.db.repositories import AnimeRepository, GenreRepository


class AnimeService:
    def __init__(self, anime_repository: AnimeRepository, genre_repository: GenreRepository):
        self.anime_repository = anime_repository
        self.genre_repository = genre_repository

    def create_anime(self, anime: AnimeDTO) -> AnimeDTO:
        anime.id = uuid4()
        return self.anime_repository.create(anime)

    def get_anime_by_id(self, anime_id: UUID) -> AnimeDTO:
        dto = self.anime_repository.get_by_id(anime_id)
        if dto is None:
            raise ValueError('Anime not found')
        return dto

    def list_anime(self) -> list[AnimeDTO]:
        return self.anime_repository.get_all()

    def update_anime(self, anime: AnimeDTO) -> AnimeDTO:
        return self.anime_repository.update(anime)

    def soft_delete_anime(self, anime_id: UUID) -> AnimeDTO:
        anime_update = self.anime_repository.get_by_id(anime_id)
        if anime_update.is_hidden:
            raise ValueError('Anime not found')
        anime_update.is_hidden = True
        return self.anime_repository.update(anime_update)

    def delete(self, anime_id: UUID):
        self.anime_repository.delete(anime_id)

    def create_genre(self, genre: str=None) -> GenreDTO:
        if genre is None:
            raise ValueError('Missing genre')
        if genre not in GenreEnum:
            raise ValueError('Genre not found')

        try:
            created_genre = self.genre_repository.create(genre)
            return created_genre
        except Exception as e:
            raise e

    def get_genre_by_id(self, genre_id: UUID) -> GenreDTO:
        dto = self.genre_repository.get_by_id(genre_id)
        if dto is None:
            raise ValueError('Genre not found')
        return dto

    def list_genres(self) -> list[GenreDTO]:
        genres = self.genre_repository.list_genres()
        return genres

    def update_genre(self, genre: GenreDTO) -> GenreDTO:
        try:
            updated_genre = self.genre_repository.update(genre)
            return updated_genre
        except Exception as e:
            raise e

    def delete_genre(self, genre_id: UUID) -> None:
        try:
            self.genre_repository.delete(genre_id)
        except Exception as e:
            raise e
