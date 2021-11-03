import dataclasses
import os


@dataclasses.dataclass(frozen=True)
class RedisSetting:
    dns: str


@dataclasses.dataclass(frozen=True)
class Settings:
    redis: RedisSetting


def settings() -> Settings:
    return Settings(redis=RedisSetting(dns=os.getenv("REDIS_DSN", "redis://redis/0")))
