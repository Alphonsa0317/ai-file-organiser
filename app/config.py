import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WATCH_DIR = os.path.join(BASE_DIR, "data", "watched")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "organized")

REDIS_HOST = "redis"
REDIS_PORT = 6379
QUEUE_NAME = "default"