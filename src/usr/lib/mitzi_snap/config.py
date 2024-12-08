import json
import logging
from typing import Union

log = logging.getLogger(__name__)

default_config = {
    "mitzi": {
        "interval_mins": 10,
    },
    "aws": {
        "access_key_id": "",
        "secret_access_key": "",
        "session_token": "",
        "region": "eu-west-1",
    },
    "take_photo": {
        "enabled": True,
        "base_dir": "/var/lib/mitzi-snap/photos",
        "max_dir_size_mb": 1024,
    },
    "upload_photos": {
        "enabled": True,
    },
    "tidy_storage": {
        "enabled": True,
        "headroom_mb": 1024 * 0.2
    },
}

config = default_config


def load_config():
    log.debug("load_config")

    log.debug(f"config: {json.dumps(config)}")
    # todo: load in from file/s3
    # todo: load in aws creds/config from file


def read_config(*keys: (str, str)) -> [Union[str, int]]:
    config_vals = [config[k1][k2] for (k1, k2) in keys]

    if any([v is None for v in config_vals]):
        raise KeyError(f"read_config failed for key(s)={list(keys)}")

    return config_vals
