import configparser
import logging
from typing import Union

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)

default_config = {
    "mitzi": {
        "interval_mins": 0,
    },
    "take_photo": {
        "enabled": True,
        "base_dir": "/var/lib/mitzi-snap/photos",
        "max_dir_size_mb": 20,
        "rotation": 0,
    },
    "upload_photos": {
        "enabled": False,
    },
    "tidy_storage": {
        "enabled": True,
        "headroom_mb": 5
    },
    "aws": {
        "access_key_id": "",
        "secret_access_key": "",
        "region": "eu-west-1",
        "bucket_name": "",
    },
}

config = configparser.ConfigParser()


def load_aws_config():
    log.debug("load_aws_config")

    global config
    
    config.read_file(open("/etc/mitzi-snap-aws.conf", "r"))


def load_config_from_s3() -> bool:
    log.debug("load_config_from_s3")

    aws_region, aws_access_key_id, aws_secret_key, aws_bucket_name = read_config(
        ("aws", "region"),
        ("aws", "access_key_id"),
        ("aws", "secret_access_key"),
        ("aws", "bucket_name"),
    )

    # Build client
    aws_config = Config(
        region_name=aws_region,
    )
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_key,
        config=aws_config
    )

    # Fetch and read the config
    try:
        log.debug(f"start remote config fetch")
        response = s3_client.get_object(
            Bucket=aws_bucket_name,
            Key='config/mitzi-snap.conf'
        )
        config_string = response['Body'].read().decode('utf-8')
        config.read_string(config_string)
        log.debug(f"completed remote config fetch")
    except ClientError as e:
        log.debug(f"remote config fetch failed")
        log.error(e)
        return False
    return True


def load_config():
    log.debug("load_config")

    global config

    load_aws_config()

    if not load_config_from_s3():
        try:
            config.read_file(open("/etc/mitzi-snap.conf", "r"))
        except Exception as e:
            log.error(f"failed to read config: {e}")
            log.error("failling back to default config")
            config.read_dict(default_config)

    log.debug(
        "loaded config:" + str({section: dict(config[section]) for section in config.sections() if section != "aws"})
    )


def read_config(*keys: (str, str)) -> [str]:
    config_vals = [config[k1][k2] for (k1, k2) in keys]

    if any([v is None for v in config_vals]):
        raise KeyError(f"read_config failed for key(s)={list(keys)}")

    return config_vals
