import configparser
import logging
from typing import Union

log = logging.getLogger(__name__)

default_config = {
    "mitzi": {
        "interval_mins": 0,
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
        "max_dir_size_mb": 20,
    },
    "upload_photos": {
        "enabled": False,
    },
    "tidy_storage": {
        "enabled": True,
        "headroom_mb": 5
    },
}

config = configparser.ConfigParser()


def load_config():
    log.debug("load_config")

    global config

    try:
        config.read_file(open("/etc/mitzi-snap.conf", "r"))
    except Exception as e:
        log.error(f"failed to read config: {e}")
        log.error("failling back to default config")
        config.read_dict(default_config)

    log.debug(
        "loaded config:" + str({section: dict(config[section]) for section in config.sections()})
    )
    # todo: load in aws creds/config from file


def read_config(*keys: (str, str)) -> [str]:
    config_vals = [config[k1][k2] for (k1, k2) in keys]

    if any([v is None for v in config_vals]):
        raise KeyError(f"read_config failed for key(s)={list(keys)}")

    return config_vals
