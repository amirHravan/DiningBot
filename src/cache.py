import redis
from redis.commands.json.path import Path


class Cache:
    RESERVE_TABLE_KEY = 'reserve_table'
    def __init__(self, host: str, port: int):
        self.cache = redis.Redis(host=host, port=port)

    def set(self, key, value):
        self.cache.set(key, value)

    def get(self, key):
        self.cache.get(key)

    def cache_reserve_table(self, reserve_table: dict):
        self.cache.json().set(self.RESERVE_TABLE_KEY, Path.root_path(), reserve_table)

    def get_reserve_table(self) -> dict:
        return self.cache.json().get(self.RESERVE_TABLE_KEY, no_escape=True)

    def del_reserve_table(self):
        self.cache.json().clear(self.RESERVE_TABLE_KEY)

    async def flush(self):
        await self.cache.flushall(asynchronous=True)
