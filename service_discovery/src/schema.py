from pydantic import BaseModel
from typing import Optional
import time


class ServiceInstanceSchema(BaseModel):
    name: str
    address: str
    port: int
    status: Optional[str] = "healthy"
    last_heartbeat: Optional[int] = int(time.time())
    registered_at: Optional[int] = int(time.time())


    def is_healthy(self):
        return self.status == "healthy"
    

    def update_heartbeat(self):
        self.last_heartbeat = int(time.time())
        self.status = "healthy"


    def mark_unhealthy(self):
        self.status = "unhealthy"