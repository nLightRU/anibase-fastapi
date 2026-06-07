import uuid

from fastapi import APIRouter, HTTPException
from anibase.presentation.schemas.anime import (
    AnimeCreateRequest,
    AnimeResponse,
    AnimeUpdateRequest,
)

router = APIRouter(prefix="/admin/anime", tags=["anime"])

fake_anime_db = {}

@router.post("/", response_model=AnimeResponse, status_code=201)
def create_anime(body: AnimeCreateRequest):
    new_anime = AnimeResponse(
        id=uuid.uuid4(),
        title=body.title,
        description=body.description,
        episodes=body.episodes,
        rating=body.rating,
        is_hidden=body.is_hidden
    )
    fake_anime_db[new_anime.id] = new_anime
    return new_anime


@router.get("/", response_model=list[AnimeResponse], status_code=200)
def list_anime():
    return list(fake_anime_db.values())


@router.get("/{anime_id}", response_model=AnimeResponse, status_code=200)
def get_anime(anime_id: uuid.UUID):
    fake_anime = fake_anime_db.get(anime_id)
    if not fake_anime:
        raise HTTPException(status_code=404, detail="Anime not found")


@router.put("/{anime_id}", response_model=AnimeResponse, status_code=200)
def update_anime(anime_id: uuid.UUID, body: AnimeUpdateRequest):
    fake_anime = fake_anime_db.get(anime_id)
    if not fake_anime:
        raise HTTPException(status_code=404, detail="Anime not found")

    update_data = body.model_dump(exclude_unset=True)
    updated_anime = fake_anime.copy(update=update_data)
    fake_anime_db[anime_id] = updated_anime
    return updated_anime


@router.delete("/{anime_id}", status_code=204)
def delete_anime(anime_id: uuid.UUID):
    fake_anime = fake_anime_db.get(anime_id)
    if not fake_anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    del fake_anime_db[anime_id]
    return