import logging
import os
from pathlib import Path

from .config import read_config

log = logging.getLogger(__name__)


def prepare():
    log.debug("prepare storage")

    base_dir, = read_config(("take_photo", "base_dir"))

    if not os.path.isdir(base_dir):
        log.debug(f"making photos dirs at {base_dir}")
        os.makedirs(os.path.join(base_dir, "queued"))
        os.makedirs(os.path.join(base_dir, "uploaded"))


def space_available() -> bool:
    base_dir, max_dir_size_mb, = read_config(
        ("take_photo", "base_dir"),
        ("take_photo", "max_dir_size_mb")
    )

    dir_current_size_mb = sum(
        os.path.getsize(os.path.join(dirpath,filename))
        for dirpath, dirnames, filenames in os.walk(base_dir)
        for filename in filenames
    ) / (1024 * 1024)

    log.debug(f"max_dir_size_mb = {max_dir_size_mb}, dir_current_size_mb = {dir_current_size_mb}")
    return dir_current_size_mb <= int(max_dir_size_mb)


def tidy():
    log.debug("tidy storage")

    enabled, headroom_mb, base_dir, max_dir_size_mb, = read_config(
        ("tidy_storage", "enabled"),
        ("tidy_storage", "headroom_mb"),
        ("take_photo", "base_dir"),
        ("take_photo", "max_dir_size_mb")
    )

    if not enabled == "True":
        log.info("skipping tidy_storage: step not enabled")
        return

    def need_to_tidy():
        dir_current_size_mb = sum(
            os.path.getsize(os.path.join(dirpath,filename))
            for dirpath, dirnames, filenames in os.walk(base_dir)
            for filename in filenames
        ) / (1024 * 1024)

        return dir_current_size_mb >= int(max_dir_size_mb) - int(headroom_mb)

    while need_to_tidy():
        if len(os.listdir(os.path.join(base_dir, 'uploaded'))):
            chosen_dir = os.path.join(base_dir, 'uploaded')
        elif len(os.listdir(os.path.join(base_dir, 'queued'))):
            chosen_dir = os.path.join(base_dir, 'queued')
        else:
            break

        files = [os.path.join(chosen_dir, f) for f in os.listdir(chosen_dir)]
        oldest_file = min(files, key=os.path.getctime)
        os.remove(oldest_file)
