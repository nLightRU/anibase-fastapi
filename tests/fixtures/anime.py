import random
import uuid
from datetime import datetime
import pytest

from anibase.application.dto import AnimeDTO
from anibase.infrastructure.db.models import Anime


@pytest.fixture
def random_anime_dto() -> AnimeDTO:
    anime_id = uuid.uuid4()
    title = f'Test Anime {datetime.now().strftime("%y-%m-%d %H:%M:%S")}'
    episodes = random.randint(1, 700)
    is_hidden = random.randint(0, 1)
    return AnimeDTO(
        id=anime_id,
        title=title,
        description='TEST TEST TEST',
        episodes=episodes,
        is_hidden=is_hidden
    )

@pytest.fixture
def random_anime() -> Anime:
    anime_id = uuid.uuid4()
    title = f'Test Anime {datetime.now().strftime("%y-%m-%d %H:%M:%S")}'
    description = f'TEST TEST TEST'
    episodes = random.randint(1, 700)
    is_hidden = random.randint(0, 1)
    return Anime(
        id=anime_id,
        title=title,
        description=description,
        episodes=episodes,
        is_hidden=is_hidden
    )