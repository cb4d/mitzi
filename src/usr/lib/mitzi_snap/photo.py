import datetime
import logging
import os

from picamera2 import Picamera2

from .config import read_config
from .storage import space_available

log = logging.getLogger(__name__)

picam2 = Picamera2()

def take_photo():
    log.debug("take_photo")

    enabled, base_dir, = read_config(
        ("take_photo", "enabled"),
        ("take_photo", "base_dir"),
    )

    if not enabled == "True":
        log.info("skipping take_photo: step not enabled")
        return

    if not space_available():
        log.info("skipping take_photo: insufficient space")
        return

    now = datetime.datetime.now(datetime.timezone.utc).time()

    filename = f"mitzi-snap-{now.isoformat()}.jpg"

    log.debug(f"snap {filename}")

    try:
        path = os.path.join(base_dir, "queued", filename)
        picam2.configure(picam2.create_still_configuration())

        picam2.start()
        picam2.capture_file(path)
        picam2.stop()
    except Exception as e:
        log.error(f"take_photo failed: {str(e)}")
