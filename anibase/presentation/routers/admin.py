from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from anibase.presentation.schemas.anime import (
    AnimeCreateRequest,
    AnimeResponse,
    AnimeUpdateRequest,
)

from anibase.application.services.anime_service import AnimeService
from anibase.application.dto.anime import AnimeDTO
from anibase.presentation.dependencies import get_anime_service, get_admin_user

router = APIRouter(prefix="/admin/anime", tags=["admin"])

@router.post("/", response_model=AnimeResponse, status_code=201)
def create_anime(
    body: AnimeCreateRequest,
    anime_service: AnimeService = Depends(get_anime_service),
    admin_id: UUID = Depends(get_admin_user),
) -> AnimeResponse:
    anime_dto = AnimeDTO.from_request_scheme(body)
    try:
        anime = anime_service.create_anime(anime_dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    genres = [g.name for g in anime.genres]
    return AnimeResponse(id=anime.id, title=anime.title, description=anime.description, genres=genres)


@router.get("/", response_model=list[AnimeResponse], status_code=200)
def list_anime(
    anime_service: AnimeService = Depends(get_anime_service),
    admin_id: UUID = Depends(get_admin_user),
) -> list[AnimeResponse]:
    anime = anime_service.list_anime()
    return [
        AnimeResponse(id=a.id, title=a.title, episodes=a.episodes, description=a.description)
        for a in anime
    ]


@router.get("/{anime_id}", response_model=AnimeResponse, status_code=200)
def get_anime(
    anime_id: UUID,
    anime_service: AnimeService = Depends(get_anime_service),
    admin_id: UUID = Depends(get_admin_user),
) -> AnimeResponse:
    try:
        anime = anime_service.get_anime_by_id(anime_id)
        return AnimeResponse(
            id=anime.id,
            title=anime.title,
            episodes=anime.episodes,
            description=anime.description,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Anime not found")


@router.put("/{anime_id}", response_model=AnimeResponse, status_code=200)
def update_anime(
    anime_id: UUID,
    body: AnimeUpdateRequest,
    anime_service: AnimeService = Depends(get_anime_service),
    admin_id: UUID = Depends(get_admin_user),

) -> AnimeResponse:
    try:
        update_dto = AnimeDTO.from_request_scheme(body)
        updated_anime = anime_service.update_anime(update_dto)
        return AnimeResponse(
            id=updated_anime.id,
            title=updated_anime.title,
            description=updated_anime.description,
            episodes=updated_anime.episodes
        )

    except ValueError:
        raise HTTPException(status_code=404, detail="Anime not found")


@router.delete("/{anime_id}", status_code=204)
def delete_anime(
    anime_id: UUID,
    anime_service: AnimeService = Depends(get_anime_service),
    admin_id: UUID = Depends(get_admin_user),
):
    try:
        _ = anime_service.soft_delete_anime(anime_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Anime not found")


@router.post('/genres')
def create_genre(
    body,
    status_code = 201
):
    ...