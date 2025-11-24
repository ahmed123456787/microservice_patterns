from fastapi.routing import APIRouter
from .service_registry import serivice_registery
from .schema import ServiceInstanceSchema
from fastapi import Response
import json


router = APIRouter()


@router.get("/services", tags=["Service Discovery"])
async def list_services():
    services = serivice_registery.get_services() 
    return Response(
        content=json.dumps({"services": services}),
        media_type="application/json",
        status_code=200
    )


@router.post("/register", tags=["Service Discovery"])
async def register_service(service: ServiceInstanceSchema):
    serivice_registery.register_service(service.name, service)
    return Response(
        content=json.dumps({"message": f"Service {service.name} registered with address {service.address}."}),
        media_type="application/json",
        status_code=201
    )


@router.post("/unregister/{service_name}/{address}", tags=["Service Discovery"])
async def unregister_service(service_name: str, address: str):

    if not address:
        serivice_registery.redis_client.hdel('services', service_name)
        return Response(
            content=json.dumps({"message": f"Service {service_name} unregistered."}),
            media_type="application/json",
            status_code=200
        )
    else:
        serivice_registery.unregister_service(service_name, address)
        return Response(
            content=json.dumps({"error": f"Service {service_name} with address {address} has been unregistered."}),
            media_type="application/json",
            status_code=404
        )
    
    
@router.post("/heartbeat/{service_name}", tags=["Service Discovery"])
async def heartbeat(service_name: str):
    address = serivice_registery.get_service(service_name)
    if address:
        return Response(
            content=json.dumps({"message": f"Service {service_name} is alive at address {address}."}),
            media_type="application/json",
            status_code=200
        )
    else:
        return Response(
            content=json.dumps({"error": f"Service {service_name} not found."}),
            media_type="application/json",
            status_code=404
        )
    