import dataclasses
import enum
import os
import pathlib
import sys
from typing import Set

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final


class SettingsError(Exception):
    pass


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


class StorageProvider(enum.Enum):
    LOCAL = enum.auto()
    S3 = enum.auto()


@dataclasses.dataclass(frozen=True)
class StorageSettings:
    provider: StorageProvider
    local_directory: pathlib.Path
    s3_access_key_id: str
    s3_secret_key: str
    s3_region_name: str
    s3_bucket_name: str


@dataclasses.dataclass(frozen=True)
class Settings:
    redis: RedisSetting
    input_store: InputStoreSetting
    io: IoSetting
    storage: StorageSettings


def load_storage_settings() -> StorageSettings:

    default_path: Final = pathlib.Path(os.getcwd()) / "storage"
    default_path.mkdir(parents=True, exist_ok=True)

    return StorageSettings(
        provider=StorageProvider[os.getenv("STORAGE_PROVIDER", "LOCAL").upper()],
        local_directory=pathlib.Path(os.getenv("LOCAL_DIRECTORY", str(default_path))),
        s3_access_key_id=os.getenv("STORAGE_S3_ACCESS_KEY_ID", ""),
        s3_secret_key=os.getenv("STORAGE_S3_SECRET_KEY", ""),
        s3_region_name=(os.getenv("STORAGE_S3_REGION_NAME", "")),
        s3_bucket_name=os.getenv("STORAGE_S3_BUCKET_NAME", ""),
    )


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
        storage=load_storage_settings(),
    )
