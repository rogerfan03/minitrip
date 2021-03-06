""" Minitrip, a filesystem integrity check tool """
import argparse
import os

from pathlib import Path
from typing import List, Optional, Set, Dict
from hashlib import sha256

from core.db import batch_write, get, put, delete

options = {}


def debug(*args, **kwargs):
    if options['verbose']:
        print(*args, **kwargs)


def main():
    """ The main function for the `minitrip` command """
    args = parser().parse_args()
    options.update(args.__dict__)
    debug(options)
    path = Path(options['path'])

    if not path.exists():
        raise RuntimeError(f"Path {path} does not exist!")

    files = walk_path(path)
    hashes = generate_hashes(files)
    present = {}
    debug('files', files)
    debug('hashes', hashes)
    for h in hashes.values():
        present[h] = get(h)
    if options['add'] and options['force']:
        to_import = {}
        for h in hashes.values():
            to_import[h] = '0'
        batch_write(to_import)
    elif options['add']:
        for h in hashes.values():
            if not int(present.get(h, default=False)):
                put(h, '0')
    elif options['check']:
        for f, h in hashes.items():
            if int(present.get(h, default=False)):
                print(f'Found a match! \nFile: {f.absolute()} \nHash:{h.hex()}')

    print('Done')


def generate_hashes(files: List[Path]) -> Dict[Path, bytes]:
    res = {}
    for file in files:
        tmp = _hash(file)
        if tmp is not None:
            res[file] = tmp
    return res


def parser():
    parse = argparse.ArgumentParser(description='Tool to check files via hashes, compare then, and so on.')
    parse.add_argument('--path', type=str, help='path to traverse, defaults to CWD', default=Path.cwd().as_posix())
    parse.add_argument('--verbose', const=True, action='store_const',
                       help='print out additional info while running')
    parse.add_argument('--add', const=True, action='store_const', help='add hashes to DB if not already present')
    parse.add_argument('--check', const=True, action='store_const',
                       help='check all hashes with db present ones for marked ones')
    parse.add_argument('--force', const=True, action='store_const',
                       help='forcefully overwrite DB hashes (used with --add)')
    return parse


def walk_path(path: Path) -> List[Path]:
    if path.is_file():
        return [path]

    res = [p for p in path.glob('**/*')]
    files = list(filter(lambda x: x.is_file(), res))
    return files


def _hash(path: Path) -> Optional[bytes]:
    if path.is_dir():
        raise NotImplementedError(f'Cannot compute hash of folder {path}!')
    res = sha256()
    try:
        file = path.open(mode='rb', buffering=8192)
        tmp = '1'
        while len(tmp) > 0:
            tmp = file.read(8192)
            res.update(tmp)
    except PermissionError:
        return None
    return res.digest()

# old approach with iterdir and so on..
# def walk_paths(paths: List[Path], searched: List[Path]) -> List[Path]:
#     # todo paths.pop()
#     for path in paths:
#         if path.is_dir():
#             for p in path.iterdir():
#                 if p.is_file():
#                     searched.append(p)
#                 else:
#                     return walk_paths(paths, searched)
#         else:
#             searched.append(path)
#
#     return searched
