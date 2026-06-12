from uuid import UUID, uuid4

from anibase.application.dto import UserAnimeDTO
from anibase.infrastructure.db.repositories import (
    AnimeRepository,
    UserRepository,
    UserAnimeRepository
)

class UserAnimeService:
    def __init__(
        self,
        entries: UserAnimeRepository = None,
        anime: AnimeRepository = None,
        users: UserRepository = None,
    ):
        if entries is None:
            raise ValueError('Missing UserAnimeRepository')
        if anime is None:
            raise ValueError('Missing AnimeRepository')
        if users is None:
            raise ValueError('Missing UserRepository')

        self.entries = entries
        self.anime = anime
        self.users = users

    def _user_is_valid(self, user_id: UUID):
        return self.users.get_by_id(user_id) is not None

    def _anime_is_valid(self, anime_id):
        return self.anime.get_by_id(anime_id) is not None

    def add_anime_to_user(self, entry: UserAnimeDTO)  -> UserAnimeDTO:
        if not (self._user_is_valid(entry.user_id) and self._anime_is_valid(entry.anime_id)):
            raise ValueError('Invalid anime or user id')
        existed_entry = self.entries.get_by_user_and_anime(entry.user_id, entry.anime_id)
        if existed_entry is None:
            return self.entries.create(
                UserAnimeDTO(
                    id=uuid4(),
                    user_id=entry.user_id,
                    anime_id=entry.anime_id,
                    status=entry.status,
                    score=entry.score
                )
            )
        else:
            return existed_entry

    def get_by_user_anime(self, user_id: UUID = None, anime_id: UUID = None):
        if not (self._user_is_valid(user_id) and self._anime_is_valid(anime_id)):
            raise ValueError('Invalid anime or user id')

        entry = self.entries.get_by_user_and_anime(user_id, anime_id)
        if entry is None:
            raise ValueError('Entry not found')

    def get_user_list(self, user_id: UUID = None) -> list[UserAnimeDTO]:
        if not self._user_is_valid(user_id):
            raise ValueError('Invalid user id')
        if user_id is None:
            raise ValueError('Missing user_id')
        return self.entries.list_by_user(user_id)

    def remove_anime_from_user(self, user_id, anime_id):
        if not (self._user_is_valid(user_id) and self._anime_is_valid(anime_id)):
            raise ValueError('Invalid anime or user id')
        entry = self.entries.get_by_user_and_anime(user_id, anime_id)
        if entry is None:
            raise ValueError('Entry not found')
        self.entries.delete(entry.id)
