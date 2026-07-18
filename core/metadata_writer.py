from pathlib import Path
import subprocess
import hashlib


# Ruta al ejecutable de ExifTool
EXIFTOOL_PATH = str(
    Path(__file__).parent.parent / "exiftool.exe"
)


def update_metadata(
        file_path: Path,
        new_name: str,
        author: str = "Saarmyx"):

    """
    Actualiza los metadatos del archivo.
    """

    title = Path(new_name).stem

    # ID único basado en nombre + ruta
    unique_id = hashlib.sha1(
        f"{title}_{file_path}".encode(
            "utf-8"
        )
    ).hexdigest()

    command = [

        EXIFTOOL_PATH,

        # TÍTULOS

        f"-Title={title}",
        f"-Subject={title}",
        f"-Description={title}",
        f"-ImageDescription={title}",
        f"-Comment={title}",
        f"-Caption-Abstract={title}",
        f"-Headline={title}",
        f"-ObjectName={title}",

        # WINDOWS EXPLORER

        f"-XPTitle={title}",
        f"-XPSubject={title}",
        f"-XPComment={title}",
        f"-XPKeywords={title}",

        # XMP

        f"-XMP-dc:Title={title}",
        f"-XMP-dc:Description={title}",
        f"-XMP-dc:Subject={title}",
        f"-XMP-dc:Identifier={unique_id}",

        # IDS INTERNOS

        f"-DocumentName={title}",
        f"-ImageUniqueID={title}",
        f"-OriginalDocumentID={unique_id}",
        f"-DocumentID={unique_id}",
        f"-InstanceID={unique_id}",
        f"-XMP-xmpMM:DocumentID={unique_id}",
        f"-XMP-xmpMM:InstanceID={unique_id}",

        # AUTORÍA

        f"-Artist={author}",
        f"-Author={author}",
        f"-Creator={author}",
        f"-OwnerName={author}",
        f"-Copyright={author}",

        # SOFTWARE

        "-Software=NexoraRename",
        "-CreatorTool=NexoraRename",

        # GUARDAR

        "-overwrite_original",

        str(file_path)
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        stderr = result.stderr

        # ERRORES MENORES IGNORADOS

        ignored_errors = [

            "Not a valid HEIC",
            "Not a valid JPG",
            "looks more like",
            "Unknown trailer",
            "SampleTable",
            "minor",
            "Warning"
        ]

        if result.returncode != 0:

            if any(
                err in stderr
                for err in ignored_errors
            ):
                return True

            print(
                f"\n[METADATA ERROR] {file_path}"
            )

            print(stderr)

            return False

        return True

    except FileNotFoundError:

        print(
            "\n[EXIFTOOL ERROR]"
        )

        print(
            "No se encontró exiftool.exe"
        )

        return False

    except Exception as e:

        print(
            f"\n[ERROR] {file_path}"
        )

        print(e)

        return False