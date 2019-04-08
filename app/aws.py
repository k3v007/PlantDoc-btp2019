import os
import traceback
from io import BytesIO

import boto3
from PIL import Image
from werkzeug.datastructures import FileStorage

S3_KEY = os.getenv('S3_KEY')
S3_SECRET = os.getenv('S3_SECRET_ACCESS_KEY')
S3_BUCKET = os.getenv('S3_BUCKET')


def get_s3_resource():
    try:
        s3_resource = boto3.resource(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )
    except:     # noqa
        traceback.print_exc()

    return s3_resource


def get_s3_client():
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )
    except:     # noqa
        traceback.print_exc()

    return s3_client



def get_bucket(bucket: str = S3_BUCKET):
    s3 = get_s3_resource()
    return s3.Bucket(bucket)


def upload_image(image_file: FileStorage, folder):
    # Resize the image before saving
    # Image size close to 640x360 or 640x480
    image = Image.open(image_file)
    max_size = 640, 480
    image.thumbnail(max_size, Image.ANTIALIAS)

    in_mem_file = BytesIO()
    image.save(in_mem_file, format=image.format)

    my_bucket = get_bucket()
    image_path = f"images/{folder}/" + image_file.filename
    my_bucket.Object(image_path).put(Body=in_mem_file.getvalue())    # noqa

    return image_path


def get_presigned_url(image_path: str):
    s3 = get_s3_client()
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': S3_BUCKET,
            'Key': image_path
        },
        ExpiresIn=3600
    )

    return url
