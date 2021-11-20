import logging
import pathlib
import sys
import time
import uuid
from typing import Any, Set

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

from owan.domain.compress import Compressor
from owan.domain.io import IoHandler
from owan.libs.storage import Storage

logger: Final = logging.getLogger("uvicorn")


class Domain:
    def __init__(
        self,
        broker: Any,  # owan.tasks.TaskQueue
        input_supported_extention: Set[str],
        output_image_compress_quality: int,
        storage: Storage,
    ) -> None:
        self.task_queue: Final = broker
        self.task_worker: Final = TaskWorker()
        self.io: Final = IoHandler()
        self.compressor: Final = Compressor(
            input_supported_extention, output_image_compress_quality
        )
        self.storage: Final = storage


class TaskWorker:
    """TaskWorker subdomain class which execute tasks asked from _TaskQueue"""

    def __init__(self) -> None:
        pass

    def predict(self) -> None:
        logger.info("predict from _TaskWorker")

    def test_predict(self, image_path: str, storage: Storage) -> None:
        time.sleep(10)

        try:
            logger.info(f"image_path: `{image_path}` is processing")
            key: Final = f"jetson/{str(uuid.uuid4())}/{pathlib.Path(image_path).name}"
            storage.store(pathlib.Path(image_path), key)
        except Exception:
            logger.error(f"failed to store `{image_path}`.")

        logger.info(f"test_predict image_path: {image_path} done.")
