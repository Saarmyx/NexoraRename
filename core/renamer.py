from pathlib import Path
from core.metadata import (
    get_best_datetime,
    VIDEO_EXTENSIONS
)


def is_motion_photo(path: Path):

    name = path.stem.lower()

    return (
        "mvimg" in name or
        "motion_photo" in name
    )


def generate_name(path: Path):

    dt = get_best_datetime(path)

    timestamp = dt.strftime(
        "%Y%m%d_%H%M%S"
    )

    if is_motion_photo(path):
        prefix = "MVIMG"

    elif path.suffix.lower() in VIDEO_EXTENSIONS:
        prefix = "VID"

    else:
        prefix = "IMG"

    return f"{prefix}_{timestamp}{path.suffix.lower()}"