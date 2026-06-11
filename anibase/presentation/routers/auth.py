import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from anibase.presentation.dependencies import get_auth_service

from anibase.presentation.schemas.auth import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    TokenResponse
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRegisterResponse, status_code=201)
def register_user(
    body: UserRegisterRequest,
    auth_service=Depends(get_auth_service)
) -> UserRegisterResponse:
    try:
        user_dto = auth_service.register_user(body.username, body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return UserRegisterResponse(
        id = user_dto.id,
        email = user_dto.email,
        username=user_dto.username
    )


@router.post("/login", response_model=TokenResponse, status_code=200)
def login(
    body: UserLoginRequest,
    auth_service=Depends(get_auth_service)
) -> TokenResponse:
    try:
        token = auth_service.authenticate_user(body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return TokenResponse(access_token=token)
