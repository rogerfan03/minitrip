from typing import Dict

from leveldb import LevelDB, LevelDBError, WriteBatch
from pathlib import Path


def _get_db() -> LevelDB:
    """
    Gets DB instance, not to be used outside, thus private
    :return: LevelDB instance
    """
    return LevelDB(Path.home() / 'minitripdb')


def batch_write(kv: Dict[str, str]):
    """
    Writes a Dictionary of Keys and Values via a WriteBatch into the DB.
    :param kv: dict of keys & values
    """
    batch = WriteBatch()
    for k, v in kv:
        batch.Put(k, v)
    _get_db().Write(batch, sync=True)


def write(key: str, value: str):
    """
    Write single key value pair into db
    :param key: key to write
    :param value: value to write
    """
    _get_db().Write(key, value)


def get(key: str) -> str:
    return _get_db().Get(key)
