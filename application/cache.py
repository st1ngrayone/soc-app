from typing import Iterable, Optional, List

import json
import redis

from config import Config
from application.entity.post import Post
from application.entity.post import PostEncoder, PostDecoder

CACHE_LIMIT = 10


class Cache:
    def __init__(self, name):
        if Config.REDIS_URL:
            self.redis = redis.from_url(Config.REDIS_URL)
        else:
            self.redis = redis.StrictRedis(
                Config.REDIS_HOST,
                charset="utf-8",
                decode_responses=True
            )
        self.hash_name = name

    def add(self, post: Post):
        self.redis.hset(self.hash_name, post.id, json.dumps(post, cls=PostEncoder))

    def get_latest_post_id(self) -> Optional[int]:
        items = self.redis.hgetall(self.hash_name)
        keys = sorted(items.keys(), reverse=True)
        if keys:
            return keys[0]

    def cache_free_space(self) -> int:
        return CACHE_LIMIT - self.redis.hlen(self.hash_name)

    def get_all(self) -> Iterable[List]:
        res = self.redis.hgetall(self.hash_name)
        if res:
            for item in res.values():
                yield json.loads(item, cls=PostDecoder)

    def replace(self, post: Post):
        self.redis.hdel(self.hash_name, post.id)
        self.add(post)

    def remove_latest(self):
        if self.cache_free_space() >= CACHE_LIMIT:
            latest_id = self.get_latest_post_id()
            if latest_id:
                self.redis.hdel(self.hash_name, latest_id)

