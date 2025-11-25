from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import time


class ServiceInstanceSchema(BaseModel):
    name: str
    address: str
    port: int
    status: Optional[str] = "healthy"
    last_heartbeat: Optional[float] = None
    registered_at: Optional[float] = None


    def __init__(self, **data):
        if 'last_heartbeat' not in data or data['last_heartbeat'] is None:
            data['last_heartbeat'] = time.time()
        if 'registered_at' not in data or data['registered_at'] is None:
            data['registered_at'] = time.time()
        super().__init__(**data)

    def is_healthy(self):
        return self.status == "healthy"
    

    def update_heartbeat(self):
        self.last_heartbeat = int(time.time())
        self.status = "healthy"


    def mark_unhealthy(self):
        self.status = "unhealthy"