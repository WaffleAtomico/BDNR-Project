"""
Connection to R2 (Amazon S3-compatible storage) for image uploads.


Credits on https://www.youtube.com/watch?v=QApVxe_JJhA
"""
import boto3
from app.logger import Logger
from fastapi import UploadFile, HTTPException
from app.lib.config import settings
from datetime import datetime
from functools import wraps
import uuid

log = Logger.Logger()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE_MB = 5

class R2Connection:
    def __init__(self):
        if not all([settings.R2_ACCESS_KEY_ID,
                    settings.R2_SECRET_ACCESS_KEY,
                    settings.R2_ENDPOINT_URL,
                    settings.R2_BUCKET_NAME,
                    settings.R2_ACCOUNT_ID]):
            log.error("R2 configuration is incomplete. Please check your environment variables.")
            raise ValueError("R2 configuration is incomplete. Please check your environment variables.")

        self.bucket_name = settings.R2_BUCKET_NAME
        self.account_id = settings.R2_ACCOUNT_ID
        self.endpoint_url = settings.R2_ENDPOINT_URL

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            endpoint_url=settings.R2_ENDPOINT_URL,
            region_name="auto"
        )

    def validate_connection(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 's3_client') or self.s3_client is None:
                log.error("R2 connection is not initialized.")
                raise HTTPException(status_code=500, detail="R2 connection is not initialized.")
            return func(self, *args, **kwargs)
        return wrapper

    def _validate_file(self, file: UploadFile):
        ext = file.filename.split(".")[-1].lower() if file.filename else ""
        if ext not in ALLOWED_EXTENSIONS and file.content_type not in [f"image/{e}" for e in ALLOWED_EXTENSIONS]:
            log.error(f"Invalid file type: {file.filename}")
            raise HTTPException(status_code=400, detail="Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.")
        
        file.file.seek(0, 2)
        file_size_mb = file.file.tell() / (1024 * 1024)
        file.file.seek(0)

        if file_size_mb > MAX_FILE_SIZE_MB:
            log.error(f"File size exceeds limit: {file_size_mb} MB")
            raise HTTPException(status_code=400, detail="File size exceeds limit (Max 5MB)")

    def _generate_unique_filename(self, original_filename: str, folder: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        ext = original_filename.split(".")[-1].lower() if original_filename else "png"
        filename = f"{timestamp}_{unique_id}.{ext}"
        return f"{folder}/{filename}"

    @validate_connection
    async def upload_image(self, file: UploadFile, folder: str = "images") -> dict:
        try:
            self._validate_file(file)
            
            file_content = await file.read()
            object_name = self._generate_unique_filename(file.filename, folder)

            metadata = {
                "original_name": file.filename,
                "upload_date": datetime.now().isoformat()
            }

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_content,
                ContentType=file.content_type,
                Metadata=metadata
            )

            log.info(f"Image {file.filename} uploaded to {object_name} in bucket {self.bucket_name}.")
            
            return {
                "key": object_name,
                "filename": file.filename,
                "content_type": file.content_type
            }

        except HTTPException as e:
            log.error(f"HTTPException during upload: {e.detail}")
            raise e
        except Exception as e:
            log.error(f"Error uploading image: {e}")
            raise HTTPException(status_code=500, detail="Internal server error during upload")

    @validate_connection
    def get_file_url(self, object_name: str) -> str:
        try:
            url = f"{self.endpoint_url}/{self.bucket_name}/{object_name}"
            log.info(f"Generated URL for {object_name}: {url}")
            return url
        except Exception as e:
            log.error(f"Error generating file URL: {e}")
            raise HTTPException(status_code=500, detail="Error generating file URL")

    @validate_connection
    def delete_file(self, object_name: str):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            log.info(f"File {object_name} deleted from bucket {self.bucket_name}.")
        except Exception as e:
            log.error(f"Error deleting file: {e}")
            raise HTTPException(status_code=500, detail="Error deleting file")


r2_conn = R2Connection()