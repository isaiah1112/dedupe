""" Python script for de-duplicating files based on different hash types
"""
import hashlib
import io
import logging
import os
import shutil
import sys
from collections import defaultdict, namedtuple

import click
from blake3 import blake3

FileSpec = namedtuple('FileSpec', ['path', 'name', 'hash'])

log = logging.getLogger('dedupe')
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s.%(module)s.%(funcName)s:%(message)s'))
log.addHandler(log_handler)
log.setLevel(logging.WARNING)
log.propagate = False  # Keeps our messages out of the root logger.


def hash_file(file: str, buffer_size: int = io.DEFAULT_BUFFER_SIZE, algorithm: str = 'md5') -> str:
    """
    Hash a file using one of the following algorythms: [md5, sha1, sha256, blake3]

    :param file: Path to file to hash
    :type file: str
    :param buffer_size: Set a buffer size to read from the file, defaults to io.DEFAULT_BUFFER_SIZE
    :type buffer_size: int, optional
    :param algorithm: Hash algorithm to use, defaults to 'md5'
    :type algorithm: str, optional
    :return: Hash of file
    :rtype: str
    """
    assert algorithm.lower() in ('md5', 'sha1', 'sha256', 'blake3')
    if algorithm.lower() == 'md5':
        file_hash = hashlib.md5()
    elif algorithm.lower() == 'sha1':
        file_hash = hashlib.sha1()
    elif algorithm.lower() == 'sha256':
        file_hash = hashlib.sha256()
    else:
        file_hash = blake3()
    with open(file, mode='rb') as f:
        buf = f.read(buffer_size)
        while len(buf) > 0:
            file_hash.update(buf)
            buf = f.read(buffer_size)
    return file_hash.hexdigest()


@click.command(epilog="""\b
Examples:
dedupe.py ~/Pictures/Wallpapers
dedupe.py --remove ~/Pictures/Wallpapers
""")
@click.version_option()
@click.option('--debug', '-d', is_flag=True, help='Enable debugging')
@click.option('--remove', '-rm', is_flag=True, help='Remove duplicate files')
@click.option('--hash', default='md5', type=click.Choice(['sha1', 'md5', 'sha256', 'blake3']), help='Hash algorithm for comparing files')
@click.argument('folder', nargs=1, type=click.Path(exists=True, file_okay=False, writable=True))
def cli(**kwargs):
    """ Utility for finding duplicate files based on different hashing algorithms.
    """
    global log
    if kwargs['debug']:
        log.setLevel(logging.DEBUG)
    log.debug(kwargs)

    if not kwargs['folder'].endswith('/'):
        log.info('Appending / to path {}'.format(kwargs['folder']))
        kwargs['folder'] = kwargs['folder'] + '/'

    files = os.listdir(kwargs['folder'])
    hashed_files = list()
    hashes = list()
    with click.progressbar(files, label=f'Building hashes of {len(files)} files', hidden=kwargs['debug']) as bar:
        for file in bar:
            f_path = kwargs['folder'] + file
            if not file.startswith('.') and not os.path.isdir(f_path):
                f_hash = hash_file(f_path, algorithm=kwargs['hash'])
                f = FileSpec(path=f_path, name=file, hash=f_hash)
                log.debug(f)
                hashed_files.append(f)
                hashes.append(f.hash)

    dupe_hashes = set([x for x in hashes if hashes.count(x) > 1])
    if len(dupe_hashes) == 0:
        click.echo('No duplicate files found')
    else:
        click.echo("Found " + str(len(dupe_hashes)) + " duplicate file(s)!")
        duplicates = defaultdict(list)
        for f in hashed_files:
            if f.hash in dupe_hashes:
                duplicates[f.hash].append(f)

        if kwargs['debug']:
            for hash, files in duplicates.items():
                log.debug({'hash': hash, 'files': [x.name for x in files]})

        for _, files in duplicates.items():
            for idx, file in enumerate(files):
                if idx > 0:
                    if kwargs['remove']:
                        os.remove(file.path)
                    else:
                        if os.path.exists(kwargs['folder'] + 'duplicates/') is False:
                            os.mkdir(kwargs['folder'] + 'duplicates/')
                        shutil.move(file.path, kwargs['folder'] + 'duplicates/' + file.name)
        if kwargs['remove']:
            click.echo("Duplicate files removed!")
        else:
            click.echo("Duplicate files moved to: " + kwargs['folder'] + 'duplicates/')
    sys.exit(0)

if __name__ == "__main__":
    click.echo('Please install the dedupe command using "pip install -u ."')
    sys.exit(1)
