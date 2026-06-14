import random
from uuid import UUID, uuid4
from pydantic import BaseModel

from anibase.application.enums import GenreEnum

_genres_test = ('Action', 'Drama', 'Comedy', 'Slice of life', 'Detective')

class GenreDTO(BaseModel):
    id: UUID
    name: GenreEnum

    @classmethod
    def create_test_genre(cls):
        genre_str = random.choice(_genres_test)
        return cls(
            id=uuid4(),
            name=GenreEnum(genre_str),
        )