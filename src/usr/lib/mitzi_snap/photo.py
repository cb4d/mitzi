import datetime
import logging

from picamzero import Camera

from .config import read_config
from .storage import space_available

log = logging.getLogger(__name__)


def take_photo():
    log.debug("take_photo")

    enabled, base_dir, max_dir_size_mb = read_config(
        ("take_photo", "enabled"),
        ("take_photo", "base_dir"),
        ("take_photo", "max_dir_size_mb")
    )

    if not enabled:
        log.info("skipping take_photo: step not enabled")
        return

    if not space_available():
        log.info("skipping take_photo: insufficient space")
        return

    now = datetime.datetime.now(datetime.timezone.utc).time()

    filename = f"mitzi-snap-{now.isoformat(microsecond=0)}.jpg"

    log.debug(f"snap {filename}")
    cam = Camera()
    cam.take_photo(base_dir / "queued" / filename)
