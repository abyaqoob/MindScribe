
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import engine
from models.entity import Base
from core.config import settings

# Routers
from routers import auth, notes, clusters, messages, users

from sqlalchemy import text

Base.metadata.create_all(bind=engine)

with engine.begin() as conn:
    conn.execute(text("ALTER TABLE clusters DROP CONSTRAINT IF EXISTS clusters_name_key;"))

app = FastAPI(
    title="Mindscribe API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials="*" not in settings.BACKEND_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/api/auth",     tags=["Auth"])
app.include_router(notes.router,    prefix="/api/notes",    tags=["Notes"])
app.include_router(clusters.router, prefix="/api/clusters", tags=["Clusters"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(users.router,    prefix="/api/users",    tags=["Users"])

allow_origins=["http://localhost:5173"]


@app.get("/api/health")
def health():
    return {"status": "ok"}