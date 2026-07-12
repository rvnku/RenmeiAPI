from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_database
from app.routes import auth


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_database()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
