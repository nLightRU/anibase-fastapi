import random
from uuid import UUID, uuid4
from pydantic import BaseModel

_genres_test = ('Action', 'Drama', 'Comedy', 'Slice of life', 'Detective')

class GenreDTO(BaseModel):
    id: UUID
    name: str

    @classmethod
    def create_test_genre(cls):
        return cls(
            id=uuid4(),
            name = random.choice(_genres_test)
        )