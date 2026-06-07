import uuid

from fastapi import APIRouter

from anibase.presentation.schemas.auth import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    TokenResponse
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRegisterResponse, status_code=201)
def register_user(body: UserRegisterRequest) -> UserRegisterResponse:
    return UserRegisterResponse(
        id=uuid.uuid4(),
        username=body.username,
        email=body.email
    )


@router.post("/login", response_model=TokenResponse, status_code=200)
def login(body: UserLoginRequest):
    return TokenResponse(
        access_token='fake-jwt-token-abc',
    )