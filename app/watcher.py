from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from collections import deque

from app.organizer import organize_file
from rq import Queue
import redis

from app.config import REDIS_HOST, REDIS_PORT, QUEUE_NAME
from app.config import WATCH_DIR, OUTPUT_DIR
from app.utils import logger


def get_redis_connection():
    for _ in range(5):
        try:
            return redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        except Exception:
            time.sleep(2)
    raise Exception("Redis not available")


os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

redis_conn = get_redis_connection()
queue = Queue(QUEUE_NAME, connection=redis_conn)


class Handler(FileSystemEventHandler):

    recent_files = deque(maxlen=100)

    def on_created(self, event):

        if event.is_directory:
            return

        if event.src_path in self.recent_files:
            return

        self.recent_files.append(event.src_path)

        logger.info(f"Detected file: {event.src_path}")

        job = queue.enqueue(
            organize_file,
            event.src_path,
            OUTPUT_DIR
        )

        logger.info(f"Queued job: {job.id}")


observer = Observer()
observer.schedule(Handler(), WATCH_DIR, recursive=False)

observer.start()

logger.info(f"Watching folder: {WATCH_DIR}")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer.stop()

observer.join()