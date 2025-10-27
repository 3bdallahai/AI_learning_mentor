import boto3 
from app.core.config import settings

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

def upload_to_s3(file_path: str, object_name:str = None ):
    s3 = get_s3_client()
    bucket = settings.AWS_BUCKET_NAME
    if object_name is None:
        object_name = file_path.split("/")[-1]

    s3.upload_file(file_path, bucket, object_name)
    file_url = f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{object_name}"
    return file_url

def delete_from_s3(s3_url:str):
    s3 = get_s3_client()
    bucket = settings.AWS_BUCKET_NAME
    key = s3_url.split(f".com/")[-1]
    s3.delete_object(Bucket = bucket, Key=key)


