"""
A module to initialize application for launching.
"""
import contextlib
import logging
import sys
from typing import Iterator

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

import owan.bootstrap
import owan.domain
import owan.settings
import owan.tasks

logger: Final = logging.getLogger("uvicorn")


def _init_storage(settings: owan.settings.StorageSettings) -> owan.libs.storage.Storage:
    def init_s3_storage() -> owan.libs.storage.S3Storage:
        s3: Final = owan.libs.storage.S3Storage(
            access_key_id=settings.s3_access_key_id,
            secret_key=settings.s3_secret_key,
            region_name=settings.s3_region_name,
            bucket_name=settings.s3_bucket_name,
            is_public=settings.s3_is_public,
            cache_max_age_in_seconds=settings.s3_cache_max_age,
        )
        s3.check_access()
        return s3

    if settings.provider == owan.settings.StorageProvider.LOCAL:
        raise NotImplementedError()
    if settings.provider == owan.settings.StorageProvider.S3:
        return init_s3_storage()
    raise owan.settings.SettingsError()


def domain_factory(settings: owan.settings.Settings) -> owan.domain.Domain:
    broker: Final = owan.tasks.Factory(broker=settings.redis.dns).broker
    storage: Final = _init_storage(settings.storage)
    return owan.domain.Domain(
        broker=broker,
        input_supported_extention=settings.io.input_supported_extensions,
        output_image_compress_quality=settings.io.output_image_compress_quality,
        storage=storage,
    )


@contextlib.contextmanager
def domain(settings: owan.settings.Settings) -> Iterator[owan.domain.Domain]:
    yield owan.bootstrap.domain_factory(settings)
