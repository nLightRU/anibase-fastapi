from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from anibase.application.dto import UserDTO
from anibase.infrastructure.db.models import User, Role


class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    @staticmethod
    def _create_dto(user: User):
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role.name
        )

    def create(self, user_dto: UserDTO) -> UserDTO:
        role =self._session.scalar(select(Role).where(Role.name==user_dto.role))
        user = User(
            id=user_dto.id,
            username=user_dto.username,
            email=user_dto.email,
            password_hash=user_dto.password_hash,
            role=role,
        )
        try:
            self._session.add(user)
            self._session.commit()
            self._session.refresh(user)
        except Exception as e:
            self._session.rollback()
            raise e
        return UserRepository._create_dto(user)

    def get_by_id(self, user_id: UUID) -> UserDTO | None:
        user_model = self._session.get(User, user_id)
        if not user_model:
            return None
        return UserRepository._create_dto(user_model)

    def get_by_email(self, email: str) -> UserDTO | None:
        user_model = self._session.scalars(select(User).where(User.email == email)).first()
        if not user_model:
            return None
        return UserRepository._create_dto(user_model)

    def get_all(self) -> list[UserDTO]:
        users = self._session.scalars(select(User)).all()
        return [UserRepository._create_dto(u)  for u in users]

    def update(self, user: UserDTO) -> UserDTO:
        user_model = self._session.scalar(select(User).where(User.id == user.id))
        role_model = self._session.scalar(select(Role).where(Role.name == user.role))
        if not user_model:
            raise ValueError('User not found')

        user_model.username = user.username
        user_model.email = user.email
        user_model.password_hash = user.password_hash
        user_model.role_id = role_model.id

        self._session.commit()

        return UserRepository._create_dto(user_model)

    def delete(self, user_id: UUID) -> None:
        user_model = self._session.get(User, user_id)
        if not user_model:
            raise ValueError('User not found')
        self._session.delete(user_model)
        self._session.commit()
