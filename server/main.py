import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncIterator

from api.records import router as record_router
from api.root import router as root_router
from core.settings import get_settings
from core.logger import get_logger


logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info(
        f"Server is started on address http://{settings.APP_HOST}:{settings.APP_PORT}"
    )
    yield
    logger.info("Server is stopped")


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(record_router)
app.include_router(root_router)


if __name__ == "__main__":
    uvicorn.run(
        app, host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.APP_RELOAD
    )
