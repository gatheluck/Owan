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

    if settings.provider == owan.settings.StorageProvider.LOCAL:
        logger.info("storage try to initialize as local only mode.")
        return owan.libs.storage.Storage(
            local_directory=settings.local_directory,
            s3_access_key_id=settings.s3_access_key_id,
            s3_secret_key=settings.s3_secret_key,
            s3_region_name=settings.s3_region_name,
            s3_bucket_name=settings.s3_bucket_name,
            local_only=True,
        )

    if settings.provider == owan.settings.StorageProvider.S3:
        logger.info("storage try to initialize as S3 mode.")
        return owan.libs.storage.Storage(
            local_directory=settings.local_directory,
            s3_access_key_id=settings.s3_access_key_id,
            s3_secret_key=settings.s3_secret_key,
            s3_region_name=settings.s3_region_name,
            s3_bucket_name=settings.s3_bucket_name,
            local_only=False,
        )

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
