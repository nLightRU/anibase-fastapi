from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from anibase.infrastructure.db.models import Role


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
