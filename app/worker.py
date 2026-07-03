from rq import Queue
from rq.worker import SimpleWorker
import redis
import time

from app.config import REDIS_HOST, REDIS_PORT, QUEUE_NAME


def get_redis_connection():
    for _ in range(5):
        try:
            return redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        except Exception:
            time.sleep(2)
    raise Exception("Redis not available")


redis_conn = get_redis_connection()
queue = Queue(QUEUE_NAME, connection=redis_conn)

worker = SimpleWorker([queue], connection=redis_conn)
worker.work()