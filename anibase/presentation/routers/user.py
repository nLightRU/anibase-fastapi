from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from anibase.application.dto import UserAnimeDTO
from anibase.presentation.schemas.user import (
    UserAnimeCreateRequest,
    UserAnimeUpdateRequest,
    UserAnimeResponse
)

from anibase.presentation.dependencies import get_current_user, get_user_anime_service
from anibase.application.services import UserAnimeService


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/anime", response_model=UserAnimeResponse, status_code=200, tags=["user"])
def add_anime_to_user(
    body: UserAnimeCreateRequest,
    user_anime_service: UserAnimeService = Depends(get_user_anime_service),
    current_user_id: UUID = Depends(get_current_user)
):
    try:
        entry_dto = UserAnimeDTO.from_request(body, current_user_id)
        entry = user_anime_service.add_anime_to_user(entry_dto)
        return UserAnimeResponse(
            id=str(entry.id),
            user_id=str(entry.user_id),
            anime_id=str(entry.anime_id),
            status=entry.status,
            score=entry.score
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/anime', response_model=list[UserAnimeResponse], status_code=200, tags=["user"])
def list_user_anime(
    current_user_id: UUID = Depends(get_current_user),
    user_anime_service: UserAnimeService = Depends(get_user_anime_service)
):
    try:
        anime_entries = user_anime_service.get_user_list(current_user_id)
        return [
            UserAnimeResponse(
                id=str(entry.id),
                user_id=str(entry.user_id),
                anime_id=str(entry.anime_id),
                status=entry.status,
                score=entry.score
            )
            for entry in anime_entries
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/anime/{entry_id}', response_model=UserAnimeUpdateRequest, status_code=200, tags=["user"])
def update_user_anime(
    entry_id: UUID,
    body: UserAnimeUpdateRequest,
    current_user_id: UUID = Depends(get_current_user),
    user_anime_service: UserAnimeService = Depends(get_user_anime_service)
):
    try:
        update_dto = UserAnimeDTO(
            id=entry_id,
            user_id=current_user_id,
            anime_id=body.anime_id,
            status=body.status,
            score=body.score
        )
        updated = user_anime_service.update_user_anime_entry(update_dto)
        return UserAnimeResponse(
            id=str(updated.id),
            user_id=str(updated.user_id),
            anime_id=str(updated.anime_id),
            status=updated.status,
            score=updated.score
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/anime/{entry_id}", status_code=204, tags=["user"])
def remove_anime_from_user(
    entry_id: UUID,
    current_user_id = Depends(get_current_user),
    user_anime_service = Depends(get_user_anime_service)
):
    try:
        user_anime_service.remove_anime_from_user(entry_id, current_user_id)
        return {'status': 'no_content'}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
