from fastapi import FastAPI
from .registery_api import router as registry_router
from contextlib import asynccontextmanager  
import asyncio
from .health_checker import health_checker


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(health_checker.start_monitoring())
    yield
    await health_checker.stop_monitoring()



app = FastAPI(
    title="Service Discovery Registry API",
    description="API for registering and discovering services in a microservices architecture.",
    lifespan=lifespan
)

app.include_router(registry_router, prefix="/api/v1")

