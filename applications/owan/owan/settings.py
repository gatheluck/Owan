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
    local_link_path: str
    s3_access_key_id: str
    s3_secret_key: str
    s3_region_name: str
    s3_bucket_name: str
    s3_is_public: bool
    s3_cache_max_age: int


@dataclasses.dataclass(frozen=True)
class Settings:
    redis: RedisSetting
    input_store: InputStoreSetting
    io: IoSetting
    storage: StorageSettings


def _load_storage_settings(prefix: str, sub_path: str) -> StorageSettings:
    DEFAULT_CACHE_MAX_AGE_IN_SECONDS: Final = 60 * 60 * 24 * 365

    path: Final = pathlib.Path(os.getcwd()) / "tmp" / sub_path
    path.mkdir(parents=True, exist_ok=True)

    return StorageSettings(
        provider=StorageProvider[os.getenv(f"{prefix}_PROVIDER", "LOCAL").upper()],
        local_directory=pathlib.Path(
            os.getenv(
                f"{prefix}_LOCAL_DIRECTORY",
                str(path),
            )
        ),
        local_link_path=os.getenv(f"{prefix}_LOCAL_LINK_PATH", f"/resource/{sub_path}"),
        s3_access_key_id=os.getenv(f"{prefix}_S3_ACCESS_KEY_ID", ""),
        s3_secret_key=os.getenv(f"{prefix}_S3_SECRET_KEY", ""),
        s3_region_name=(os.getenv(f"{prefix}_S3_REGION_NAME", "")),
        s3_bucket_name=os.getenv(f"{prefix}_S3_BUCKET_NAME", ""),
        s3_is_public=bool(int(os.getenv(f"{prefix}_S3_IS_PUBLIC", "1"))),
        s3_cache_max_age=int(
            os.getenv(
                f"{prefix}_S3_CACHE_MAX_AGE",
                str(DEFAULT_CACHE_MAX_AGE_IN_SECONDS),
            )
        ),
    )


def load_storage_settings() -> StorageSettings:
    return _load_storage_settings(prefix="PRIVATE_STORAGE", sub_path="private")


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
