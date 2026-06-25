import os
from pathlib import Path

from core.renamer import generate_name


SUPPORTED_EXTENSIONS = {

    # Imágenes

    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".heic",
    ".bmp",
    ".tiff",

    # Vídeos

    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".webm",
    ".3gp",
    ".m4v"
}


def scan_folders(
        folders,
        progress_callback=None):

    """
    Escanea múltiples carpetas.

    Devuelve una lista de diccionarios:

    {
        "path": ruta_completa,
        "folder": carpeta,
        "original": nombre_actual,
        "new": nuevo_nombre,
        "size": tamaño
    }
    """

    results = []

    all_files = []

    # =================================================
    # RECOPILAR ARCHIVOS
    # =================================================

    for folder in folders:

        folder = Path(folder)

        if not folder.exists():
            continue

        for root, _, files in os.walk(folder):

            root = Path(root)

            for filename in files:

                file_path = root / filename

                ext = (
                    file_path.suffix
                    .lower()
                )

                if ext in SUPPORTED_EXTENSIONS:
                    all_files.append(
                        file_path
                    )

    total = len(all_files)

    if total == 0:
        return results

    # =================================================
    # PROCESAR ARCHIVOS
    # =================================================

    for index, file_path in enumerate(
            all_files,
            start=1):

        try:

            new_name = generate_name(
                file_path
            )

            file_info = {

                "path": file_path,

                "folder": str(
                    file_path.parent
                ),

                "original":
                    file_path.name,

                "new":
                    new_name,

                "size":
                    file_path.stat().st_size
            }

            results.append(
                file_info
            )

        except Exception as e:

            print(
                f"[SCAN ERROR] "
                f"{file_path}"
            )

            print(e)

        # ==========================================
        # PROGRESO
        # ==========================================

        if progress_callback:

            progress = int(
                (index / total) * 100
            )

            progress_callback(
                progress
            )

    return results


def count_supported_files(
        folders):
    """
    Cuenta archivos compatibles.
    """

    total = 0

    for folder in folders:

        folder = Path(folder)

        if not folder.exists():
            continue

        for root, _, files in os.walk(folder):

            for filename in files:

                ext = (
                    Path(filename)
                    .suffix
                    .lower()
                )

                if ext in SUPPORTED_EXTENSIONS:
                    total += 1

    return total