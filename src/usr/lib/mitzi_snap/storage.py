import logging
import os

from .config import read_config

log = logging.getLogger(__name__)


def prepare():
    log.debug("prepare storage")

    base_dir, = read_config(("take_photo", "base_dir"))

    dir_scan = os.scandir(base_dir)
    if not dir_scan.is_dir():
        log.debug(f"making photos dirs at {base_dir}")
        os.makedirs(base_dir / "queued")
        os.makedirs(base_dir / "uploaded")


def space_available() -> bool:
    base_dir, max_dir_size_mb, = read_config(
        ("take_photo", "base_dir"),
        ("take_photo", "max_dir_size_mb")
    )

    dir_scan = os.scandir(base_dir)
    dir_current_size = dir_scan.stat().st_size / (1024 * 1024)

    log.debug(f"max_dir_size_mb = {max_dir_size_mb}, dir_current_size = {dir_current_size}")
    return dir_current_size >= max_dir_size_mb


def tidy():
    log.debug("tidy storage")

    enabled, headroom_mb, base_dir, max_dir_size_mb, = read_config(
        ("tidy_storage", "enabled"),
        ("tidy_storage", "headroom_mb"),
        ("take_photo", "base_dir"),
        ("take_photo", "max_dir_size_mb")
    )

    if not enabled:
        log.info("skipping tidy_storage: step not enabled")
        return

    def need_to_tidy():
        dir_scan = os.scandir(base_dir)
        dir_current_size_mb = dir_scan.stat().st_size / (1024 * 1024)
        return dir_current_size_mb >= max_dir_size_mb - headroom_mb

    while need_to_tidy():
        if len(os.listdir(base_dir / 'uploaded')):
            chosen_dir = base_dir / 'uploaded'
        elif len(os.listdir(base_dir / 'queued')):
            chosen_dir = base_dir / 'queued'
        else:
            break

        files = [chosen_dir / f for f in os.listdir(chosen_dir)]
        oldest_file = min(files, key=os.path.getctime)
        os.remove(oldest_file)
