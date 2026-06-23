from pathlib import Path
import os

from core.renamer import generate_name


SUPPORTED_EXTENSIONS = {

    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".heic",
    ".bmp",
    ".tiff",

    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".webm",
    ".3gp",
    ".m4v"
}


def scan_folder(folder):

    results = []

    folder = Path(folder)

    for root, _, files in os.walk(folder):

        root = Path(root)

        for file in files:

            file_path = root / file

            if (
                file_path.suffix.lower()
                not in SUPPORTED_EXTENSIONS
            ):
                continue

            new_name = generate_name(file_path)

            results.append({
                "path": file_path,
                "original": file_path.name,
                "new": new_name
            })

    return results