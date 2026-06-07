from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from anibase.infrastructure.config import settings

engine = create_engine(url=settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)