import uuid

from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, CheckConstraint, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

POSTGRES_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata_obj = MetaData(naming_convention=POSTGRES_NAMING_CONVENTION)


class Base(DeclarativeBase):
    metadata = metadata_obj


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    users: Mapped[list['User']] = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)

    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('roles.id'), nullable=False)
    role: Mapped[Role] = relationship('Role', back_populates='users')

    anime_list: Mapped[list['UserAnime']] = relationship('UserAnime', back_populates='user')

    @classmethod
    def create_test_user(
        cls,
        role_id:uuid.UUID=None, id: uuid.UUID = None,
        username: str='test_user', email: str='test@anibase.com',
        password_hash: str='secret123',
    ):
        if role_id is None:
            raise ValueError('Missing role_id for test user')
        if id is None:
            id=uuid.uuid4(),
        return cls(
            id=id,
            username=username,
            email=email,
            password_hash=password_hash,
            role_id=role_id
        )


class Anime(Base):
    __tablename__ = 'anime'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title:Mapped[str] = mapped_column(String(200), nullable=False)
    episodes: Mapped[int] = mapped_column(Integer, nullable=True)
    description:Mapped[str] = mapped_column(Text, nullable=True)
    is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user_anime_list: Mapped[list['UserAnime']] = relationship('UserAnime', back_populates='anime')

    @classmethod
    def create_test_anime(cls,
        anime_id: uuid.UUID = None,
        title: str='Test Anime',
        episodes: int=10,
        description: str='Test Anime description',
        is_hidden: bool=False
    ):
        if anime_id is None:
            anime_id = uuid.uuid4()
        return cls(
            id=anime_id,
            title=title,
            episodes=episodes,
            description=description,
            is_hidden=is_hidden,
        )


class UserAnimeStatus(Base):
    __tablename__ = 'user_anime_statuses'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    user_anime_entries: Mapped[list['UserAnime']] = relationship(
        'UserAnime',
        back_populates='status'
    )


class UserAnime(Base):
    __tablename__ = 'user_anime'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    anime_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('anime.id'), nullable=False)
    status_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('user_anime_statuses.id'),
        nullable=False
    )
    score: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint('score BETWEEN 1 AND 10', name='check_user_anime_score'),
        nullable=True
    )

    user: Mapped['User'] = relationship('User', back_populates='anime_list')
    anime: Mapped['Anime'] = relationship('Anime', back_populates='user_anime_list')
    status: Mapped['UserAnimeStatus'] = relationship(
        'UserAnimeStatus',
        back_populates='user_anime_entries'
    )
