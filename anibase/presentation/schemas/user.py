from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class UserAnimeStatusEnum(str, Enum):
   planning = 'planning'
   watching = 'watching'
   on_hold = 'on_hold'
   completed = 'completed'
   dropped = 'dropped'


class UserAnimeCreateRequest(BaseModel):
    anime_id: str
    status: UserAnimeStatusEnum = UserAnimeStatusEnum.planning
    score: Optional[int] = Field(None, ge=1, le=10)


class UserAnimeUpdateRequest(BaseModel):
    anime_id: str
    status: UserAnimeStatusEnum
    score: Optional[int] = Field(None, ge=1, le=10)


class UserAnimeResponse(BaseModel):
    id: str
    user_id: str
    anime_id: str
    status: UserAnimeStatusEnum
    score: Optional[int] = None
