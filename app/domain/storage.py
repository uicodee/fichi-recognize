# import boto3
#
# ENDPOINT = "https://storage.yandexcloud.net"
#
# session = boto3.Session(
#     aws_access_key_id="YCAJE8uHr3tXrw5NyP9fFsRjk",
#     aws_secret_access_key="YCOjybstskomaNuV-iZeMD_sOAXRRc-VJiU_wgdr",
#     region_name="ru-central1",
# )
#
# s3 = session.client("s3", endpoint_url=ENDPOINT)
import uuid

import boto3
from fastapi import File

from app.config import Settings


class S3StorageService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.storage.endpoint,
            region_name=settings.storage.region,
            aws_access_key_id=settings.storage.access_key,
            aws_secret_access_key=settings.storage.secret_key,
            # endpoint_url="https://storage.yandexcloud.net",
            # region_name="ru-central1",
            # aws_access_key_id="YCAJE8uHr3tXrw5NyP9fFsRjk",
            # aws_secret_access_key="YCOjybstskomaNuV-iZeMD_sOAXRRc-VJiU_wgdr",
        )

    async def upload(self, file: File):
        filename = str(uuid.uuid4()) + "." + (file.filename.split("."))[-1]
        self.client.upload_fileobj(file.file, self.settings.storage.bucket_id, filename)
        path = (
            f"{self.settings.storage.endpoint}/"
            f"{self.settings.storage.bucket_id}"
            f"/{filename}"
        )
        return path
