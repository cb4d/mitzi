import configparser
import logging
from typing import Union

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


def load_config():
    log.debug("load_config")

    global config
    
    config.read_file(open("/etc/mitzi-snap-aws.conf", "r"))

    # todo: load in config from aws before local fallback
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
