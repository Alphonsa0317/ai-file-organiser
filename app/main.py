from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest
import os
from app.config import OUTPUT_DIR

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI File Organizer Running"}


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )


@app.get("/files")
def get_files():

    base_dir = OUTPUT_DIR
    
    
    if not os.path.exists(base_dir):
        return {"status": "success", "data": {}}



    data = {}

    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)

        if os.path.isdir(folder_path):
            data[folder] = os.listdir(folder_path)

    return {
    "status": "success",
    "data": data
}
