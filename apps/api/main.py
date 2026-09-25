from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes.health import router as health_router
from routes.projects import router as projects_router
from routes.repositories import router as repositories_router
from routes.tasks import router as tasks_router
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for the CodeForge AI autonomous software engineering platform.",
)


app.include_router(
    health_router,
    prefix="/api/v1",
)
app.include_router(
    projects_router,
    prefix="/api/v1",
)
app.include_router(
    repositories_router,
    prefix="/api/v1",
)
app.include_router(
    tasks_router,
    prefix="/api/v1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)