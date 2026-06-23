from pathlib import Path
import hashlib

from core.history import (
    load_history,
    save_history
)


def sha256_file(path):

    sha = hashlib.sha256()

    with open(path, "rb") as f:

        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):
            sha.update(chunk)

    return sha.hexdigest()


def generate_conflict_name(
    directory,
    base_name,
    extension
):

    counter = 1

    while True:

        candidate = directory / (
            f"{base_name}_{counter:03d}{extension}"
        )

        if not candidate.exists():
            return candidate

        counter += 1


def execute_rename(files):

    history = []

    known_hashes = {}

    stats = {
        "renamed": 0,
        "duplicates": 0,
        "conflicts": 0,
        "errors": 0
    }

    for file in files:

        try:

            source = Path(file["path"])

            if not source.exists():
                continue

            destination = (
                source.parent /
                file["new"]
            )

            # mismo nombre

            if source == destination:
                continue

            # hash global

            source_hash = sha256_file(source)

            if source_hash in known_hashes:

                stats["duplicates"] += 1
                continue

            known_hashes[source_hash] = source

            # conflicto local

            if destination.exists():

                destination_hash = (
                    sha256_file(destination)
                )

                if destination_hash == source_hash:

                    stats["duplicates"] += 1
                    continue

                destination = (
                    generate_conflict_name(
                        destination.parent,
                        destination.stem,
                        destination.suffix
                    )
                )

                stats["conflicts"] += 1

            source.rename(destination)

            history.append({
                "old": str(source),
                "new": str(destination)
            })

            stats["renamed"] += 1

        except Exception as e:

            print(e)

            stats["errors"] += 1

    previous = load_history()

    previous.extend(history)

    save_history(previous)

    return stats