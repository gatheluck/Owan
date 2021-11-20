import logging
import pathlib
import shutil
import sys
from typing import Optional

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

import boto3.exceptions
import boto3.session

logger: Final = logging.getLogger("uvicorn")


class Error(Exception):
    pass


class LocalStorage:
    """Provide access to Local Strage."""

    def __init__(self, directory: pathlib.Path) -> None:
        self.directory: Final = directory
        self._prepare_directory()

    def _prepare_directory(self) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)

    def store(
        self,
        file_path: pathlib.Path,
        key: str,
    ) -> None:
        logger.info(f"try to store local: `{file_path}` to `{key}`.")
        try:
            save_path: Final = self.directory / key
            save_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, save_path)
        except Exception:
            message: Final = "Falied to store local storage."
            logger.error(message)
            raise Error(message)


class S3Storage:
    """Provide access to Amazon S3."""

    def __init__(
        self,
        access_key_id: str,
        secret_key: str,
        region_name: str,
        bucket_name: str,
    ) -> None:
        self._bucket_name: Final = bucket_name
        self._region_name: Final = region_name
        self._bucket: Final = boto3.resource(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key,
        ).Bucket(bucket_name)

    def store(
        self,
        file_path: pathlib.Path,
        key: str,
    ) -> None:
        """Store (upload) file-like object to S3.

        Args:
            key (Key):
            source (IO[bytes]):
            content_type (str):

        Raises:
            NoSuchBucketError: Bucket does not exist.
            Error:

        """
        logger.info(f"try to store S3: `{file_path}` to `{key}`.")
        try:
            self._bucket.upload_file(
                Filename=str(file_path),
                Key=key,
            )
        except Exception:
            message: Final = "Falied to store S3."
            logger.error(message)
            raise Error(message)


class Storage:
    def __init__(
        self,
        local_directory: pathlib.Path,
        s3_access_key_id: str,
        s3_secret_key: str,
        s3_region_name: str,
        s3_bucket_name: str,
        local_only: bool = False,
    ) -> None:
        self._local_only: Final = local_only
        self._local_storage: Final = LocalStorage(local_directory)
        self._s3_storage = self._init_s3_storage(
            s3_access_key_id,
            s3_secret_key,
            s3_region_name,
            s3_bucket_name,
            self._local_only,
        )

    def _init_s3_storage(
        self,
        s3_access_key_id: str,
        s3_secret_key: str,
        s3_region_name: str,
        s3_bucket_name: str,
        local_only: bool,
    ) -> Optional[S3Storage]:
        if local_only:
            logger.info("init storage as local only mode.")
            return None

        try:
            return S3Storage(
                s3_access_key_id,
                s3_secret_key,
                s3_region_name,
                s3_bucket_name,
            )
        except Exception:
            logger.error("falied to initialize S3.")
            return None

    def store(
        self,
        file_path: pathlib.Path,
        key: str,
    ) -> None:
        """Store file-like object."""
        logger.info(f"store data to storage. `self._local_only`: {self._local_only}.")
        if self._local_only:
            self._local_storage.store(file_path, key)
        else:
            try:
                self._s3_storage.store(file_path, key)  # type: ignore
            except Exception:
                logger.warn("Try to store S3 but failed. Try to store local storage.")
                self._local_storage.store(file_path, key)
