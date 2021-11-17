import base64
import copy
import dataclasses
import sys
import urllib.parse
import uuid
from typing import IO, Any, Callable, cast

if sys.version_info >= (3, 8):
    from typing import Final, Protocol
else:
    from typing_extensions import Final, Protocol

import boto3.exceptions
import boto3.session
import botocore.client
import botocore.errorfactory
import botocore.exceptions


class Error(Exception):
    pass


class NoSuchDirectoryError(Error):
    """Specified directory does not exist."""


class NoSuchBucketError(NoSuchDirectoryError):
    """Specified bucket does not exist in S3."""


@dataclasses.dataclass(frozen=True)
class Key:
    """Use for store data to Storage.

    Each keys have own namespace. So there is no conflict between files
    which have exactly same name. If you want to create the keys which
    have same namespace, please use `fork` method.

    """

    namespace: uuid.UUID
    filename: str

    @classmethod
    def deserialize(cls, serialized: str) -> "Key":
        """Create Key class instance from string gerenated by `serialize`."""
        namespace, filename = serialized.split(".", 1)

        return cls(
            uuid.UUID(bytes=base64.urlsafe_b64decode(namespace)),
            base64.urlsafe_b64decode(filename).decode(),
        )

    def serialize(self) -> str:
        """Convert instance to URL safe string.

        Note:
            We join the namespace and filename by `.` because it does not
            used by base64.urlsafe_b64decode.

        """
        return ".".join(
            [
                base64.urlsafe_b64encode(self.namespace.bytes).decode(),
                base64.urlsafe_b64encode(self.filename.encode()).decode(),
            ]
        )

    @classmethod
    def generate(cls, filename: str) -> "Key":
        """Generate Key."""
        return cls(uuid.uuid4(), filename)

    def fork(self, filename: str) -> "Key":
        """Generate Key which has same namespace."""
        return Key(namespace=self.namespace, filename=filename)


class Storage(Protocol):
    def store(self, key: Key, source: IO[bytes], content_type: str) -> None:
        """Store file-like object."""
        ...

    def generate_link(self, key: Key) -> str:
        """Generate URL to access the file."""
        ...

    def __hash__(self) -> int:
        ...

    def __eq__(self, other: Any) -> bool:
        ...


# Becasue boto3 create class dynamically, it is difficult to read type for type hint.
# So we use Any.
S3Client = Any


def _key_to_path(key: Key) -> str:
    return "{}.{}".format(
        base64.urlsafe_b64encode(key.namespace.bytes).decode(),
        urllib.parse.quote(key.filename),
    )


class S3Storage:
    """Provide access to Amazon S3."""

    def __init__(
        self,
        access_key_id: str,
        secret_key: str,
        region_name: str,
        bucket_name: str,
        is_public: bool,
        cache_max_age_in_seconds: int,
    ) -> None:
        self._bucket_name: Final = bucket_name
        self._region_name: Final = region_name
        self._client: Final = self._create_s3_client(
            access_key_id, secret_key, region_name
        )
        self._linker: Final = self._get_linker(is_public)
        self._base_store_extra_args: Final = {
            "CacheControl": f"max-age={cache_max_age_in_seconds}"
        }
        if is_public:
            self._base_store_extra_args["ACL"] = "public-read"

    def _get_linker(self, is_public: bool) -> Callable[[str], str]:
        return self._link_publicly if is_public else self._link_privatly

    def check_access(self) -> None:
        """Check accessibility to S3.

        Raises:
            botocore.exceptions.ClientError: When authentication fail.

        """
        self._client.get_bucket_location(Bucket=self._bucket_name)

    def _create_s3_client(
        self, access_key_id: str, secret_key: str, region_name: str
    ) -> S3Client:
        """Create S3 service clients.

        This method is thin wrap method of boto3.session.Session.
        For detail please check offical docs;
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html?highlight=session#boto3.session.Session

        Args:
            access_key_id (str): AWS access key ID.
            secret_key (str): AWS secret access key.
            region_name (str): Default region when creating new connections.

        Returns:
            S3Client: Service client instance.

        """
        return boto3.session.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key,
            region_name=region_name,
        ).client("s3")

    def store(
        self,
        key: Key,
        source: IO[bytes],
        content_type: str = "binary/octet-stream",
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
        extra_args: Final = copy.copy(self._base_store_extra_args)
        extra_args["ContentType"] = content_type
        try:
            self._client.upload_fileobj(
                source,
                self._bucket_name,
                _key_to_path(key),
                ExtraArgs=extra_args,
            )
        except botocore.exceptions.ClientError as e:
            error: Final = e.response["Error"]
            if error["Code"] == "NoSuchBucket":
                message = f"Bucket: {self._bucket_name} does not exist."
                raise NoSuchBucketError(message) from e
            raise Error(error["Code"], e["Message"]) from e

    def _link_privatly(self, key: str) -> str:
        return cast(
            str,
            self._client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": self._bucket_name,
                    "Key": key,
                },
                HttpMethod="GET",
            ),
        )

    def _link_publicly(self, key: str) -> str:
        return (
            f"https://{self._bucket_name}."
            f"s3-{self._region_name}.amazonaws.com/{key}"
        )

    def generate_link(self, key: Key) -> str:
        return self._linker(_key_to_path(key))

    def __hash__(self) -> int:
        return hash((self._bucket_name, self._region_name))

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._bucket_name == other._bucket_name
            and self._region_name == other._region_name
        )
