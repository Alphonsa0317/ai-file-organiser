import os
import shutil
import hashlib
import time
from prometheus_client import Counter,Histogram
from app.utils import logger


# Metrics
processed_files = Counter(
    'processed_files_total',
    'Total processed files'
)

failed_files = Counter(
    'failed_files_total',
    'Total failed file processing'
)

processing_time = Histogram(
    'file_processing_seconds',
    'Time taken to process file'
)


processed_hashes = set()

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()


def wait_for_file_complete(file_path, retries=5):
    last_size = -1

    for _ in range(retries):
        if not os.path.exists(file_path):
            return False

        current_size = os.path.getsize(file_path)

        if current_size == last_size:
            return True

        last_size = current_size
        time.sleep(1)

    return False


CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv"],
    "Code": [".py", ".js", ".java"],
    "Archives": [".zip", ".rar"],
    "Executables": [".exe"],
    "Binary": [".bin", ".iso"]
}


def organize_file(file_path, output_dir):
    start_time = time.time()

    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return

        # Wait until file is fully written
        
        if not wait_for_file_complete(file_path):
            logger.warning(f"Incomplete file skipped: {file_path}")
            return


        # Duplicate check using hash
        file_hash = get_file_hash(file_path)

        if file_hash in processed_hashes:
            logger.info(f"Duplicate skipped: {file_path}")
            return

        processed_hashes.add(file_hash)

        _, extension = os.path.splitext(file_path)

        for category, extensions in CATEGORIES.items():
            if extension.lower() in extensions:

                category_path = os.path.join(output_dir, category)
                os.makedirs(category_path, exist_ok=True)

                file_name = os.path.basename(file_path)
                destination = os.path.join(category_path, file_name)

                # Handle duplicate names
                counter = 1
                while os.path.exists(destination):
                    name, ext = os.path.splitext(file_name)
                    destination = os.path.join(
                        category_path, f"{name}_{counter}{ext}"
                    )
                    counter += 1

                shutil.move(file_path, destination)

                processed_files.inc()
                logger.info(f"Moved {file_name} → {category}")
                return

        logger.warning(f"Unknown file type: {file_path}")

    
    except Exception as e:
        failed_files.inc()
        logger.error(f"Error processing {file_path}: {e}")

    finally:
        processing_time.observe(time.time() - start_time)

