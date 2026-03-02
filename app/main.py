from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import api_router
from app.core.config import settings
from app.db.prisma_client import prisma_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma_db.connect()
    yield
    await prisma_db.disconnect()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Mount the static frontend interface at /chat
app.mount("/chat", StaticFiles(directory="frontend", html=True), name="frontend")

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}!"}
