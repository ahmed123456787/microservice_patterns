import redis
from .config import Settings
from .schema import ServiceInstanceSchema
import time
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




class ServiceRegistry:
    def __init__(self, redis_host='redis', redis_port=6379):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)


    def register_service(self, service_name: str, service_instance: ServiceInstanceSchema):

        # test existing of the service
        if self.redis_client.hexists('services', service_name):
            instances = self.redis_client.hget('services', service_name)
            instances = json.loads(instances)
            instances.append(service_instance.__dict__)

            self.redis_client.hset('services', service_name, json.dumps(instances))

        else:
            pass
            self.redis_client.hset('services', service_name, json.dumps([service_instance.__dict__]))


    def find_instance_of_service(self, service_name: str, ip_address: str):
        instances = self.get_service(service_name)
        if instances:
            for instance in instances:
                if instance['ip_address'] == ip_address:
                    return instance
        return None


    def get_service(self, service_name: str):
        if self.redis_client.hexists('services', service_name):
            instances = self.redis_client.hget('services', service_name)
            instances = json.loads(instances)
            return instances
        return None
    

    def get_services(self):
        services = self.redis_client.hgetall('services')
        result = {}
        for key, value in services.items():
            result[key.decode('utf-8')] = json.loads(value)
        return result
    
    
    def unregister_service(self, service_name: str,ip_address: str):
        instances = self.get_service(service_name)
        instances = [inst for inst in instances if inst['ip_address'] != ip_address]
        if instances:
            self.redis_client.hset('services', service_name, json.dumps(instances))
        else:
            self.redis_client.hdel('services', service_name)

    
    def heartbeat(self, service_name: str, ip_address: str):
        instances = self.get_service(service_name)
        if instances:
            for instance in instances:
                if instance['ip_address'] == ip_address:
                    instance['last_heartbeat'] = int(time.time())
                    instance['status'] = 'healthy'
            self.redis_client.hset('services', service_name, json.dumps(instances))
            return True
        return False
    

    def mark_unhealthy(self, service_name: str, ip_address: str):
        instances = self.get_service(service_name)
        if instances:
            for instance in instances:
                if self.find_instance_of_service(service_name, ip_address):
                    instance['status'] = 'unhealthy'
            self.redis_client.hset('services', service_name, json.dumps(instances))
            return True
        return False



serivice_registery = ServiceRegistry(Settings.REDIS_HOST, Settings.REDIS_PORT)