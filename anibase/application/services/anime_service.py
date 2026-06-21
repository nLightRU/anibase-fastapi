from uuid import UUID, uuid4

from anibase.application.enums import GenreEnum
from anibase.application.dto import AnimeDTO, GenreDTO
from anibase.infrastructure.db.repositories import AnimeRepository, GenreRepository


class AnimeService:
    def __init__(self, anime_repository: AnimeRepository, genre_repository: GenreRepository):
        self.anime_repo = anime_repository
        self.genres_repo = genre_repository

    def create_anime(self, anime: AnimeDTO) -> AnimeDTO:
        anime.id = uuid4()
        all_genres = {g.name : g for g in self.genres_repo.list_genres()}
        for g in anime.genres:
            if g.name in all_genres.keys():
                g.id = all_genres[g.name].id
            else:
                raise ValueError(f'Genre {g.name.value} not found')

        return self.anime_repo.create(anime)

    def get_anime_by_id(self, anime_id: UUID) -> AnimeDTO:
        dto = self.anime_repo.get_by_id(anime_id)
        if dto is None:
            raise ValueError('Anime not found')
        return dto

    def list_anime(self) -> list[AnimeDTO]:
        return self.anime_repo.get_all()

    def update_anime(self, anime: AnimeDTO) -> AnimeDTO:
        all_genres = {g.name: g for g in self.genres_repo.list_genres()}
        for g in anime.genres:
            if g.name in all_genres.keys():
                g.id = all_genres[g.name].id
        return self.anime_repo.update(anime)

    def soft_delete_anime(self, anime_id: UUID) -> AnimeDTO:
        anime_update = self.anime_repo.get_by_id(anime_id)
        if anime_update.is_hidden:
            raise ValueError('Anime not found')
        anime_update.is_hidden = True
        return self.anime_repo.update(anime_update)

    def delete(self, anime_id: UUID):
        self.anime_repo.delete(anime_id)

    def create_genre(self, genre: str=None) -> GenreDTO:
        if genre is None:
            raise ValueError('Missing genre')
        if genre not in GenreEnum:
            raise ValueError('Genre not found')

        try:
            created_genre = self.genres_repo.create(genre)
            return created_genre
        except Exception as e:
            raise e

    def get_genre_by_id(self, genre_id: UUID) -> GenreDTO:
        dto = self.genres_repo.get_by_id(genre_id)
        if dto is None:
            raise ValueError('Genre not found')
        return dto

    def list_genres(self) -> list[GenreDTO]:
        genres = self.genres_repo.list_genres()
        return genres

    def update_genre(self, genre: GenreDTO) -> GenreDTO:
        try:
            updated_genre = self.genres_repo.update(genre)
            return updated_genre
        except Exception as e:
            raise e

    def delete_genre(self, genre_id: UUID) -> None:
        try:
            self.genres_repo.delete(genre_id)
        except Exception as e:
            raise e
