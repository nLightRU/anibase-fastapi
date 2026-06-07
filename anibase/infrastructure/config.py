from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql://anibase_user:anibasepass@localhost:5432/anibase_dev'
    JWT_SECRET: str = 'change-me-in-prod'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = '.env'
        extra = 'ignore'

settings = Settings()
