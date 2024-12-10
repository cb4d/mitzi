#!/usr/bin/python3
import logging
import time

from .config import load_config, read_config
from .log import setup_log
from .photo import take_photo
from .storage import prepare, tidy
from .upload import upload_queued_photos

log = logging.getLogger(__name__)


def sleep_or_exit():
    log.debug("sleep_or_exit")

    interval_mins, = read_config(("mitzi", "interval_mins"))

    if int(interval_mins) == 0:
        log.info("exiting: interval_mins=0")
        exit(0)
    else:
        log.debug(f"sleeping for interval_mins={interval_mins}")
        time.sleep(60 * int(interval_mins))


if __name__ == "__main__":
    setup_log()

    while True:
        load_config()
        prepare()
        take_photo()
        upload_queued_photos()
        tidy()
        sleep_or_exit()
