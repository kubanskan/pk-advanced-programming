import redis
import json


class QueueClient:
    def __init__(self, host='redis', port=6379):
        self.client = redis.Redis(host=host, port=port, db=0)

    def push_task(self, queue_name: str, task_data: dict):
        self.client.rpush(queue_name, json.dumps(task_data))

    def pop_task(self, queue_name: str):
        return self.client.blpop(queue_name)