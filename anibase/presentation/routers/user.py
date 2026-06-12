from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from anibase.application.dto import UserAnimeDTO
from anibase.presentation.schemas.user import (
    UserAnimeCreateRequest,
    UserAnimeUpdateRequest,
    UserAnimeResponse
)

from anibase.presentation.dependencies import get_current_user, get_user_anime_service

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/anime", response_model=UserAnimeResponse, status_code=200, tags=["user"])
def add_anime_to_user(
    body: UserAnimeCreateRequest,
    user_anime_service = Depends(get_user_anime_service),
    current_user_id = Depends(get_current_user),
):
    try:
        entry_dto = UserAnimeDTO.from_request(body, current_user_id)
        entry = user_anime_service.add_anime_to_user(entry_dto)
        return UserAnimeResponse(
            id=str(entry.id),
            user_id=str(entry.user_id),
            anime_id=str(entry.anime_id),
            status=entry.status,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
