"""Find duplicate files using different hash algorithms."""

import hashlib
import io
import logging
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import click
from blake3 import blake3


@dataclass(frozen=True, slots=True)
class FileSpec:
    path: Path
    name: str
    hash: str


log = logging.getLogger("dedupe")
log_handler = logging.StreamHandler()
log_handler.setFormatter(
    logging.Formatter(
        "%(levelname)s:%(name)s.%(module)s.%(funcName)s:%(message)s"
    )
)
log.addHandler(log_handler)
log.setLevel(logging.WARNING)
log.propagate = False


def hash_file(
    file: str | Path,
    buffer_size: int = io.DEFAULT_BUFFER_SIZE,
    algorithm: str = "md5",
) -> str:
    """Hash a file with MD5, SHA-1, SHA-256, or BLAKE3."""
    normalized_algorithm = algorithm.lower()
    if normalized_algorithm not in ("md5", "sha1", "sha256", "blake3"):
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    file_hash = (
        blake3()
        if normalized_algorithm == "blake3"
        else hashlib.new(normalized_algorithm)
    )
    with Path(file).open("rb") as source:
        while chunk := source.read(buffer_size):
            file_hash.update(chunk)
    return file_hash.hexdigest()


@click.command(
    epilog="""\b
Examples:
dedupe ~/Pictures/Wallpapers
dedupe --remove ~/Pictures/Wallpapers
"""
)
@click.version_option()
@click.option("--debug", "-d", is_flag=True, help="Enable debugging")
@click.option("--remove", "-rm", is_flag=True, help="Remove duplicate files")
@click.option(
    "--hash",
    "algorithm",
    default="md5",
    type=click.Choice(["sha1", "md5", "sha256", "blake3"]),
    help="Hash algorithm for comparing files",
)
@click.argument(
    "folder",
    nargs=1,
    type=click.Path(exists=True, file_okay=False, writable=True),
)
def cli(folder: str, debug: bool, remove: bool, algorithm: str) -> None:
    """Find duplicate files in a directory."""
    log.setLevel(logging.DEBUG if debug else logging.WARNING)
    log.debug(
        {"folder": folder, "debug": debug, "remove": remove, "hash": algorithm}
    )

    folder_path = Path(folder)
    files = list(folder_path.iterdir())
    files_by_hash: defaultdict[str, list[FileSpec]] = defaultdict(list)
    with click.progressbar(
        files,
        label=f"Building hashes of {len(files)} files",
        hidden=debug,
    ) as bar:
        for path in bar:
            if path.name.startswith(".") or not path.is_file():
                continue
            file_spec = FileSpec(
                path=path,
                name=path.name,
                hash=hash_file(path, algorithm=algorithm),
            )
            log.debug(file_spec)
            files_by_hash[file_spec.hash].append(file_spec)

    duplicate_groups = {
        file_hash: group
        for file_hash, group in files_by_hash.items()
        if len(group) > 1
    }
    if not duplicate_groups:
        click.echo("No duplicate files found")
        return

    click.echo(f"Found {len(duplicate_groups)} duplicate file(s)!")
    if debug:
        for file_hash, group in duplicate_groups.items():
            log.debug({"hash": file_hash, "files": [file.name for file in group]})

    duplicates_path = folder_path / "duplicates"
    for group in duplicate_groups.values():
        for file_spec in group[1:]:
            if remove:
                file_spec.path.unlink()
            else:
                duplicates_path.mkdir(exist_ok=True)
                shutil.move(str(file_spec.path), str(duplicates_path / file_spec.name))

    if remove:
        click.echo("Duplicate files removed!")
    else:
        click.echo(f"Duplicate files moved to: {duplicates_path}/")


if __name__ == "__main__":
    cli()
