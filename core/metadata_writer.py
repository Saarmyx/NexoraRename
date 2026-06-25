from pathlib import Path
import subprocess


EXIFTOOL_PATH = "exiftool"


def update_metadata(
        file_path: Path,
        new_name: str,
        author: str = "Saarmyx"):

    """
    Actualiza los metadatos internos
    para que coincidan con el nuevo nombre.
    """

    title = Path(new_name).stem

    command = [

        EXIFTOOL_PATH,

        # Información general

        f"-Title={title}",
        f"-Subject={title}",
        f"-Description={title}",
        f"-ImageDescription={title}",
        f"-Comment={title}",

        # Windows Explorer

        f"-XPTitle={title}",
        f"-XPSubject={title}",
        f"-XPComment={title}",

        # IPTC

        f"-ObjectName={title}",
        f"-Headline={title}",

        # XMP

        f"-XMP-dc:Title={title}",
        f"-XMP-dc:Description={title}",

        # Autoría

        f"-Artist={author}",
        f"-Author={author}",
        f"-Creator={author}",
        f"-Copyright={author}",
        f"-OwnerName={author}",

        # Software

        "-Software=NexRename Media",
        "-CreatorTool=NexRename Media",

        # Sobrescribir archivo original

        "-overwrite_original",

        str(file_path)
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        return True

    except subprocess.CalledProcessError as e:

        print(
            f"[METADATA ERROR] "
            f"{file_path}"
        )

        print(e.stderr)

        return False

    except Exception as e:

        print(
            f"[ERROR] {file_path}"
        )

        print(e)

        return False