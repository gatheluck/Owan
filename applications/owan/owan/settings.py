import dataclasses
import os
import pathlib


@dataclasses.dataclass(frozen=True)
class RedisSetting:
    dns: str


@dataclasses.dataclass(frozen=True)
class InputStoreSetting:
    path: pathlib.Path


@dataclasses.dataclass(frozen=True)
class Settings:
    redis: RedisSetting
    input_store: InputStoreSetting


def settings() -> Settings:
    return Settings(
        redis=RedisSetting(dns=os.getenv("REDIS_DSN", "redis://redis/0")),
        input_store=InputStoreSetting(
            path=pathlib.Path(os.getenv("INPUT_STORE_DIR_PATH", "./tmp/input_store"))
        ),
    )
