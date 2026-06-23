from pathlib import Path
from datetime import datetime

from PIL import Image, ExifTags

try:
    from pymediainfo import MediaInfo
except Exception:
    MediaInfo = None


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".heic",
    ".bmp",
    ".tiff",
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".webm",
    ".3gp",
    ".m4v",
}


EXIF_TAGS = {
    "DateTimeOriginal",
    "DateTimeDigitized",
    "DateTime"
}


def get_exif_datetime(path: Path):

    try:
        with Image.open(path) as img:

            exif = img.getexif()

            if not exif:
                return None

            for tag_id, value in exif.items():

                tag = ExifTags.TAGS.get(tag_id)

                if tag in EXIF_TAGS:

                    try:
                        return datetime.strptime(
                            str(value),
                            "%Y:%m:%d %H:%M:%S"
                        )
                    except:
                        pass

    except:
        pass

    return None


def get_video_datetime(path: Path):

    if not MediaInfo:
        return None

    try:

        media_info = MediaInfo.parse(str(path))

        for track in media_info.tracks:

            if track.track_type == "General":

                fields = [
                    track.recorded_date,
                    track.tagged_date,
                    track.file_last_modification_date
                ]

                for value in fields:

                    if value:

                        try:
                            return datetime.fromisoformat(
                                value.replace("UTC ", "")
                            )
                        except:
                            pass

    except:
        pass

    return None


def get_best_datetime(path: Path):

    ext = path.suffix.lower()

    if ext in IMAGE_EXTENSIONS:

        dt = get_exif_datetime(path)

        if dt:
            return dt

    elif ext in VIDEO_EXTENSIONS:

        dt = get_video_datetime(path)

        if dt:
            return dt

    try:
        return datetime.fromtimestamp(
            path.stat().st_mtime
        )
    except:
        return datetime.now()