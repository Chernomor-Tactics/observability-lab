"""Idempotently create the metrics bucket, waiting for MinIO to become ready."""
import time
from pathlib import Path
from minio import Minio

root = Path(__file__).resolve().parents[1]
credentials = {}
for line in (root / ".env").read_text().splitlines():
    key, separator, value = line.partition("=")
    if separator and key in {"MINIO_ROOT_USER", "MINIO_ROOT_PASSWORD"}:
        credentials[key] = value.strip().strip("\"'")
client = Minio("127.0.0.1:9000", access_key=credentials["MINIO_ROOT_USER"],
               secret_key=credentials["MINIO_ROOT_PASSWORD"], secure=False)
for attempt in range(30):
    try:
        if not client.bucket_exists("metrics"):
            client.make_bucket("metrics")
        break
    except Exception:
        if attempt == 29:
            raise
        time.sleep(2)
print("Bucket metrics is ready")
