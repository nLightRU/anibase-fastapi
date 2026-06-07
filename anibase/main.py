from fastapi import FastAPI
from anibase.presentation.routers import admin_router, auth_router

app = FastAPI(
    title='Anibase',
    version='0.1.0'
)

app.include_router(auth_router)
app.include_router(admin_router)

@app.get('/health')
def health_check():
    return {'status': 'ok'}