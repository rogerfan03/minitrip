""" Minitrip, a filesystem integrity check tool """
import argparse
import os

from pathlib import Path
from typing import List
from hashlib import sha256

from core.db import batch_write, get, write


def main():
    """ The main function for the `minitrip` command """
    print("Hello world1")
    return 0


def parser():
    parse = argparse.ArgumentParser(description='Tool to check files via hashes, compare then, and so on.')
    parse.add_argument('path', metavar='str', type=str, nargs=1, help='path to traverse, defaults to CWD',
                       default=Path.cwd())
    pass


def walk_paths(paths: List[Path]) -> List[Path]:
    pass
