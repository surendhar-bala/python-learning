import os

import boto3
from dotenv import load_dotenv

load_dotenv()


R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")


r2_client = boto3.client(
    "s3",
    endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name="auto",
)

def upload_file_to_r2(
    file,
    object_key: str
):
    r2_client.upload_fileobj(
        file.file,
        R2_BUCKET_NAME,
        object_key
    )

    return object_key

def download_file_from_r2(
    object_key: str,
    local_path: str
):
    r2_client.download_file(
        R2_BUCKET_NAME,
        object_key,
        local_path
    )