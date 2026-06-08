from contextlib import asynccontextmanager
from fastapi import FastAPI
from anibase.presentation.routers import admin_router, auth_router
from anibase.infrastructure.db.models import Base
from anibase.infrastructure.db.session import engine


@asynccontextmanager
async def lifespan():
    Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title='Anibase',
    version='0.1.0',
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(admin_router)


@app.get('/health')
def health_check():
    return {'status': 'ok'}