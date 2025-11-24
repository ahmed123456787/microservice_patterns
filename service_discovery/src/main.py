from fastapi import FastAPI
from .registery_api import router as registry_router



app = FastAPI(
    title="Service Discovery Registry API",
    description="API for registering and discovering services in a microservices architecture.",
)

app.include_router(registry_router, prefix="/api/v1")

