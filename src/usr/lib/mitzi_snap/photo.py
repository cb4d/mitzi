import datetime
import json
import logging
import os

from picamera2 import Picamera2
import piexif

from .config import read_config
from .storage import space_available

log = logging.getLogger(__name__)

picam2 = Picamera2()

def take_photo():
    log.debug("take_photo")

    enabled, base_dir, rotation = read_config(
        ("take_photo", "enabled"),
        ("take_photo", "base_dir"),
        ("take_photo", "rotation"),
    )

    rotation = int(rotation)

    if not enabled == "True":
        log.info("skipping take_photo: step not enabled")
        return

    if not space_available():
        log.info("skipping take_photo: insufficient space")
        return

    now = datetime.datetime.now(datetime.timezone.utc)

    filename = f"mitzi-snap-{now.isoformat()}.jpg"

    if rotation == 90:
        exif_orientation = 6
    elif rotation == 180:
        exif_orientation = 3
    elif rotation == 270:
        exif_orientation = 8
    else:
        exif_orientation = 1

    exif_with_rotation = {"0th": {piexif.ImageIFD.Orientation: exif_orientation}}
    log.debug(f"exif data: {json.dumps(exif_with_rotation)}")

    log.debug(f"snap {filename}")

    try:
        path = os.path.join(base_dir, "queued", filename)
        picam2.configure(picam2.create_still_configuration())

        picam2.start()
        picam2.capture_file(path, exif_data=exif_with_rotation)
        picam2.stop()
    except Exception as e:
        log.error(f"take_photo failed: {str(e)}")
    

