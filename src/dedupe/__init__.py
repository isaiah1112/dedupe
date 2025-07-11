""" Python script for de-duplicating files based on md5 hash
"""
import hashlib
import logging
import os
import shutil
import sys
from collections import defaultdict, namedtuple

import click

FileSpec = namedtuple('FileSpec', ['path', 'name', 'hash'])

log = logging.getLogger('dedupe')
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s.%(module)s.%(funcName)s:%(message)s'))
log.addHandler(log_handler)
log.setLevel(logging.WARNING)
log.propagate = False  # Keeps our messages out of the root logger.


def sha1_hash(file: str, buffer_size: int = 81920) -> str:
    """ Create an sha1 hash of a file

    :param file: Path to file to hash
    :type file: str, required
    :param buffer_size: Number of bytes to read from file at a time (default: 81920)
    :type buffer_size: int, optional
    :return: SHA1 hex hash
    :rtype: str
    """
    sha1 = hashlib.sha1()
    with open(file, 'rb') as f:
        buf = f.read(buffer_size)
        while len(buf) > 0:
            sha1.update(buf)
            buf = f.read(buffer_size)
    return sha1.hexdigest()

def md5_file(file: str, buffer_size: int = 65536) -> str:
    """ Create an md5 hash of a file

    :param file: Path to file to hash
    :type file: str, required
    :param buffer_size: Number of bytes to read from file at a time (default: 65536)
    :type buffer_size: int, optional
    :return: MD5 hex hash
    :rtype: str
    """
    md5 = hashlib.md5()
    with open(file, 'rb') as f:
        buf = f.read(buffer_size)
        while len(buf) > 0:
            md5.update(buf)
            buf = f.read(buffer_size)
    return md5.hexdigest()


@click.command(epilog="""\b
Examples:
dedupe.py ~/Pictures/Wallpapers
dedupe.py --remove ~/Pictures/Wallpapers
""")
@click.version_option()
@click.option('--debug', '-d', is_flag=True, help='Enable debugging')
@click.option('--remove', '-rm', is_flag=True, help='Remove duplicate files')
@click.option('--sha1', '-S', is_flag=True, help='Use sha1 algorithum for comparing files')
@click.argument('folder', nargs=1, type=click.Path(exists=True, file_okay=False, writable=True))
def cli(**kwargs):
    """ Utility for finding duplicate files based on md5 hashes.

    You can also use sha1 hashes to compare files if you wish by using the `--sha1`
    flag.
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
    with click.progressbar(files, label=f'Building hashes of {len(files)} files') as bar:
        for file in bar:
            f_path = kwargs['folder'] + file
            if not file.startswith('.') and not os.path.isdir(f_path):
                f_hash = sha1_hash(f_path) if kwargs['sha1'] else md5_file(f_path)
                f = FileSpec(path=f_path, name=file, hash=f_hash)
                hashed_files.append(f)
                hashes.append(f.hash)

    dupe_hashes = set([x for x in hashes if hashes.count(x) > 1])
    if len(dupe_hashes) == 0:
        click.echo('No duplicate files found')
    else:
        print("Found " + str(len(dupe_hashes)) + " duplicate file(s)!")
        duplicates = defaultdict(list)
        for f in hashed_files:
            if f.hash in dupe_hashes:
                duplicates[f.hash].append(f)

        if kwargs['debug']:
            for hash, files in duplicates.items():
                click.echo('-' * 16)
                click.echo(hash)
                click.echo('-' * 16)
                click.echo('\n'.join([x.name for x in files]))

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
            print("Duplicate files removed!")
        else:
            print("Duplicate files moved to: " + kwargs['folder'] + 'duplicates/')
    sys.exit(0)

if __name__ == "__main__":
    print('Please install the dedupe command using "pip install -u ."')
    sys.exit(1)
