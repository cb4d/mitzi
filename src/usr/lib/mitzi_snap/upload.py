import logging
import os

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from .config import read_config

log = logging.getLogger(__name__)


def upload_file_to_s3(file_name: str, bucket: str, object_name=None) -> bool:
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    aws_region, aws_access_key_id, aws_secret_key, = read_config(
        ("aws", "region"),
        ("aws", "access_key_id"),
        ("aws", "secret_access_key"),
    )

    # Build client
    config = Config(
        region_name=aws_region,
    )
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_key,
        config=config
    )

    # Upload the file
    try:
        log.debug(f"start upload for {file_name}")
        s3_client.upload_file(file_name, bucket, object_name)
        log.debug(f"completed upload for {file_name}")
    except ClientError as e:
        log.error(e)
        return False
    return True


def upload_queued_photos():
    log.debug("upload_queued_photos")

    enabled, base_dir, aws_bucket_name, = read_config(
        ("upload_photos", "enabled"),
        ("take_photo", "base_dir"),
        ("aws", "bucket_name"),
    )

    if not enabled == "True":
        log.info("skipping upload_queued_photos: step not enabled")
        return

    for rel_f in os.listdir(os.path.join(base_dir, "queued")):
        queued_file = os.path.join(base_dir, "queued", rel_f)

        if upload_file_to_s3(queued_file, aws_bucket_name, f"uploads/{rel_f}"):
            os.rename(queued_file, os.path.join(base_dir, "uploaded", rel_f))
