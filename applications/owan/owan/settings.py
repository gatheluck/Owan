import dataclasses
import os
import pathlib
from typing import Set


@dataclasses.dataclass(frozen=True)
class RedisSetting:
    dns: str


@dataclasses.dataclass(frozen=True)
class InputStoreSetting:
    path: pathlib.Path


@dataclasses.dataclass(frozen=True)
class IoSetting:
    input_supported_extensions: Set[str]
    output_image_compress_quality: int


@dataclasses.dataclass(frozen=True)
class Settings:
    redis: RedisSetting
    input_store: InputStoreSetting
    io: IoSetting


def settings() -> Settings:
    return Settings(
        redis=RedisSetting(dns=os.getenv("REDIS_DSN", "redis://redis/0")),
        input_store=InputStoreSetting(
            path=pathlib.Path(os.getenv("INPUT_STORE_DIR_PATH", "./tmp/input_store"))
        ),
        io=IoSetting(
            input_supported_extensions={".png", ".jpg", ".jpeg"},
            output_image_compress_quality=30,
        ),
    )
