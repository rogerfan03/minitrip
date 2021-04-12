from typing import Dict, Union, Optional

from leveldb import LevelDB, LevelDBError, WriteBatch
from pathlib import Path


STB = Union[str, bytes]


def b(s: STB, enc: str = 'ascii') -> bytes:
    """
    converts likely str obj to bytes (ascii encoding by default)
    :param s: string to convert (may also be bytes-like already)
    :param enc: default ascii, str encoding
    :return: string converted to bytes or just bytes if it already was such.
    """
    if type(s) == bytes:
        return s
    return bytes(s, encoding=enc)


def _get_db() -> LevelDB:
    """
    Gets DB instance, not to be used outside, thus private
    :return: LevelDB instance
    """
    return LevelDB((Path.home() / 'minitripdb').as_posix(), create_if_missing=True, paranoid_checks=True)


def batch_write(kv: Dict[STB, STB]):
    """
    Writes a Dictionary of Keys and Values via a WriteBatch into the DB.
    :param kv: dict of keys & values
    """
    batch = WriteBatch()
    for k, v in kv.items():
        batch.Put(b(k), b(v))
    _get_db().Write(batch, sync=True)


def put(key: STB, value: STB):
    """
    Write single key value pair into db
    :param key: key to write
    :param value: value to write
    """
    _get_db().Put(b(key), b(value))


def get(key: STB) -> Optional[str]:
    try:
        return _get_db().Get(b(key)).decode('ascii')
    except KeyError:
        return None


def delete(key: STB):
    try:
        return _get_db().Delete(b(key), sync=True)
    except KeyError:
        return None
