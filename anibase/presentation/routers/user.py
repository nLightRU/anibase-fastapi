from fastapi import APIRouter, HTTPException
from anibase.presentation.schemas.user import (
    UserAnimeCreateRequest,
    UserAnimeUpdateRequest,
    UserAnimeResponse
)

from anibase.presentation.routers.admin import fake_anime_db

fake_user_anime_db = {}

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/anime", response_model=UserAnimeResponse, status_code=200, tags=["user"])
def add_anime_to_user(body: UserAnimeCreateRequest):
    anime = fake_anime_db.get(body.anime_id)
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")

    return 200
