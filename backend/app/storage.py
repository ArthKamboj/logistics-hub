import os
from minio import Minio
from datetime import timedelta
from app.config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

def ensure_bucket_exists():
    if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
        minio_client.make_bucket(settings.MINIO_BUCKET_NAME)

def get_presigned_put_url(object_name: str) -> str:
    ensure_bucket_exists()
    return minio_client.presigned_put_object(
        settings.MINIO_BUCKET_NAME,
        object_name,
        expires=timedelta(minutes=15)
    )