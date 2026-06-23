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


def scan_folders(folders, progress_callback=None):

    results = []

    all_files = []

    # recopilar archivos primero

    for folder in folders:

        folder = Path(folder)

        for root, _, files in os.walk(folder):

            root = Path(root)

            for file in files:

                file_path = root / file

                if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    all_files.append(file_path)

    total = len(all_files)

    for index, file_path in enumerate(all_files, start=1):

        try:

            new_name = generate_name(file_path)

            results.append({
                "path": file_path,
                "original": file_path.name,
                "new": new_name
            })

        except Exception as e:
            print(e)

        if progress_callback:
            progress = int((index / total) * 100)
            progress_callback(progress)

    return results