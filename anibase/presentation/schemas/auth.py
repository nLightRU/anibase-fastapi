import uuid

from pydantic import BaseModel, EmailStr, Field

class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)


class UserRegisterResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'