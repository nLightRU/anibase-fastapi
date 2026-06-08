from pydantic import BaseModel
from uuid import UUID

class UserDTO(BaseModel):
    id: UUID
    username: str
    password_hash: str
    email: str
    role: str

    class Config:
        from_attributes = True
