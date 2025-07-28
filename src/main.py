from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI

from src.router import router
from src.database.database import get_async_session
from src.database.db_init import seed_initial_currencies
from src.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting app")
    async for session in get_async_session():
        await seed_initial_currencies(session)
        break
    yield
    logger.info("Finishing app")


app = FastAPI(lifespan=lifespan)

app.include_router(router)
