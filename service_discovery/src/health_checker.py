import asyncio
from .service_registry import serivice_registery
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthChecker:
    def __init__(self, check_interval:int = 5):
        self.check_interval = check_interval
        self.running = False


    async def start_monitoring(self):
        logger.info("Starting health checker...")
        self.running = True
        while self.running:
            try:
                await self._check_services()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logging.error(f"Error during health check: {e}")
                await asyncio.sleep(self.check_interval)


    async def _check_services(self):
        services = serivice_registery.get_services()

        for service_name, instances in services.items():
            for instance in instances:
                ip_address = instance['address']
                last_heartbeat = instance.get('last_heartbeat', 0)
                current_time = time.time()  
                time_diff = current_time - last_heartbeat

                if time_diff > self.check_interval * 3:
                    serivice_registery.mark_unhealthy(service_name, ip_address)

    
    async def stop_monitoring(self):
        logger.info("Stopping health checker...")
        self.running = False

        
health_checker = HealthChecker()