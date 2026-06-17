from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from anibase.application.dto import AnimeDTO, GenreDTO
from anibase.infrastructure.db.models import Anime, Genre


class AnimeRepository:
    def __init__(self, session: Session):
        self._session = session

    @staticmethod
    def _create_dto(anime_model: Anime):
        return AnimeDTO(
            id=anime_model.id,
            title=anime_model.title,
            description=anime_model.description,
            episodes=anime_model.episodes,
            is_hidden=anime_model.is_hidden,
            genres=[GenreDTO(id=g.id, name=g.name) for g in anime_model.genres]
        )

    def create(self, anime: AnimeDTO) -> AnimeDTO | None:
        genre_names = [g.name for g in anime.genres]
        genres = self._session.scalars(
            select(Genre)
            .where(Genre.name.in_(genre_names))
        ).all()
        anime_model = Anime(
            id=anime.id,
            title=anime.title,
            description=anime.description,
            episodes=anime.episodes,
            is_hidden=anime.is_hidden,
            genres=list(genres),
        )
        self._session.add(anime_model)
        self._session.commit()
        self._session.refresh(anime_model)
        return AnimeRepository._create_dto(anime_model)

    def get_by_id(self, anime_id: UUID) -> AnimeDTO | None:
        anime_model = self._session.get(Anime, anime_id)
        if not anime_model:
            return None
        return AnimeRepository._create_dto(anime_model)

    def get_all(self) -> list[AnimeDTO]:
        result = self._session.scalars(select(Anime))
        return [AnimeRepository._create_dto(a) for a in result]

    def update(self, anime_dto: AnimeDTO) -> AnimeDTO | None:
        anime_model = self._session.get(Anime, anime_dto.id)
        if not anime_model:
            raise ValueError('Anime not found')

        anime_model.title = anime_dto.title
        anime_model.description = anime_dto.description
        anime_model.episodes = anime_dto.episodes
        anime_model.is_hidden = anime_dto.is_hidden

        if anime_dto.genres:
            new_genres = self._session.scalars(
                select(Genre)
                .where(Genre.id.in_([g.id for g in anime_dto.genres]))
            )
            anime_model.genres.clear()
            anime_model.genres.extend(new_genres)
        elif anime_dto.genres is None:
            anime_model.genres.clear()

        self._session.commit()
        self._session.refresh(anime_model)

        return AnimeRepository._create_dto(anime_model)

    def delete(self, anime_id: UUID):
        anime_model = self._session.get(Anime, anime_id)
        if not anime_model:
            raise ValueError('Anime not found')

        self._session.delete(anime_model)
        self._session.commit()
