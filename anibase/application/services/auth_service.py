from uuid import uuid4

from anibase.infrastructure.db.repositories import UserRepository, RoleRepository
from anibase.application.dto import UserDTO
from anibase.infrastructure.auth.password_hasher import PasswordHasher
from anibase.infrastructure.auth.jwt_handler import create_access_token


class AuthService:
    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository):
        self.hasher = PasswordHasher()
        self.user_repository = user_repository
        self.role_repository = role_repository

    def register_user(self, username: str, email: str, password: str) -> UserDTO:
        if self.user_repository.get_by_email(email) is not None:
            raise ValueError('Email already exists')

        role_name = self.role_repository.get_by_name('user').name

        user_dto = UserDTO(
            id = uuid4(),
            username=username,
            password_hash=self.hasher.get_password_hash(password),
            email=email,
            role=role_name
        )

        created = self.user_repository.create(user_dto)

        return created

    def authenticate_user(self, email: str, password: str) -> str:
        user_dto = self.user_repository.get_by_email(email)
        if user_dto is None or (not self.hasher.verify_password(password, user_dto.password_hash)):
            raise ValueError('Invalid credentials')

        return create_access_token({'sub': str(user_dto.id.hex), 'role': user_dto.role})