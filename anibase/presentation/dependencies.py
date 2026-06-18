from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from anibase.infrastructure.auth.jwt_handler import decode_access_token
from anibase.infrastructure.db.session import SessionLocal
from anibase.infrastructure.db.repositories import (
    UserRepository,
    AnimeRepository,
    UserAnimeRepository,
    RoleRepository,
    GenreRepository
)

from anibase.application.services import  (
    AuthService,
    AnimeService,
    UserAnimeService
)

bearer = HTTPBearer()


def get_session():
    sess = SessionLocal()
    try:
        yield sess
    finally:
        sess.close()


def get_user_repo(sess: Session = Depends(get_session)):
    return UserRepository(sess)


def get_role_repo(sess: Session = Depends(get_session)):
    return RoleRepository(sess)


def get_anime_repo(sess: Session = Depends(get_session)):
    return AnimeRepository(sess)


def get_genre_repo(sess: Session = Depends(get_session)):
    return GenreRepository(sess)


def get_user_anime_repo(sess: Session = Depends(get_session)):
    return UserAnimeRepository(sess)


def get_auth_service(
        user_repo: UserRepository = Depends(get_user_repo),
        role_repo: RoleRepository = Depends(get_role_repo)
):
    return AuthService(user_repo, role_repo)


def get_anime_service(
    anime_repo: AnimeRepository = Depends(get_anime_repo),
    genre_repo: GenreRepository = Depends(get_genre_repo)
):
    return AnimeService(anime_repo, genre_repo)


def get_user_anime_service(
    anime_repo: AnimeRepository = Depends(get_anime_repo),
    users_repo: UserRepository = Depends(get_user_repo),
    user_anime_repo: UserAnimeRepository = Depends(get_user_anime_repo)
) -> UserAnimeService:
    return UserAnimeService(entries=user_anime_repo, anime=anime_repo, users=users_repo)


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer),
        user_repo: UserRepository = Depends(get_user_repo)
) -> UUID:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user_id_str = payload.get("sub")
    user_id = UUID(user_id_str)
    user_dto = user_repo.get_by_id(user_id)
    if not user_dto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_dto.id


def get_admin_user(
        current_user_id: UUID = Depends(get_current_user),
        user_repo: UserRepository = Depends(get_user_repo)
) -> UUID:
    user_dto = user_repo.get_by_id(current_user_id)
    if user_dto.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin user required")

    return user_dto.id