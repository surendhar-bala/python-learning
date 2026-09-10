import uuid

from fastapi import Depends, FastAPI, UploadFile, File, HTTPException
from celery.result import AsyncResult

from app.rate_limit import rate_limit

from .database import Base, engine
from . import models
from .jobs import process_excel
from .worker import celery_app
from .storage import upload_file_to_r2
from .redis import redis_client

app = FastAPI()


# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/test")
def home():
    redis_client.set("test", "hello")
    print(redis_client.get("test"))
    return {
        "message": "FastAPI Background Job Demo"
    }

@app.get(
    "/api/data",
    dependencies=[Depends(rate_limit)]
)
def get_data():

    return {
        "message": "Success"
    }
@app.post("/upload-excel")
async def upload_excel(
    file: UploadFile = File(...)
):

    # Validate file type
    if not file.filename.endswith(".xlsx"):

        raise HTTPException(
            status_code=400,
            detail="Only .xlsx files are supported"
        )

    # Generate unique filename
    file_id = str(uuid.uuid4())

    # R2 object key
    object_key = f"queue-file/{file_id}.xlsx"

    # Upload file directly to Cloudflare R2
    upload_file_to_r2(
        file,
        object_key
    )

    # Send R2 object key to Celery
    task = process_excel.delay(
        object_key
    )

    return {
        "message": "File uploaded successfully",
        "job_id": task.id,
        "status": "queued",
        "file": object_key
    }


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):

    result = AsyncResult(
        job_id,
        app=celery_app
    )

    response = {
        "job_id": job_id,
        "status": result.status
    }

    if result.ready():

        response["result"] = result.result

    return response
