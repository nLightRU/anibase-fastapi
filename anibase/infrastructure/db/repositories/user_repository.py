from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from anibase.infrastructure.db.models import User, Role


class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, user_id: UUID) -> type[User] | None:
        return self._session.get(User, user_id)
        # return self._session.scalars(select(User).where(User.id == user_id)).first()

    def get_by_email(self, email: str) -> User | None:
        return self._session.scalars(select(User).where(User.email == email)).first()

    def list_all(self) -> list[type[User]]:
        return self._session.scalars(select(User)).all()

    def create(self, user: User) -> User | None:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def update(self, user: User) -> User | None:
        self._session.merge(user)
        self._session.commit()
        return user

    def delete(self, user: User) -> User | None:
        self._session.delete(user)
        self._session.commit()


class RoleRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, role_id: UUID) -> type[Role] | None:
        return self._session.get(Role, role_id)

    def get_by_name(self, name: str) -> Role | None:
        return self._session.scalar(select(Role).where(Role.name == name))

    def create(self, role: Role) -> Role:
        self._session.add(Role)
        self._session.commit()
        self._session.refresh(Role)
        return role