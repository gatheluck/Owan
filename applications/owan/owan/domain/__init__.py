import logging
import sys
import time
from typing import Any

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

from owan.domain.io import IoHandler

logger: Final = logging.getLogger("uvicorn")


class Domain:
    def __init__(
        self,
        broker: Any,  # owan.tasks.TaskQueue
    ) -> None:
        self.task_queue: Final = broker
        self.task_worker: Final = TaskWorker()
        self.io: Final = IoHandler()


class TaskWorker:
    """TaskWorker subdomain class which execute tasks asked from _TaskQueue"""

    def __init__(self) -> None:
        pass

    def predict(self) -> None:
        logger.info("predict from _TaskWorker")

    def test_predict(self, image_path: str) -> None:
        time.sleep(10)
        logger.info(f"test_predict image_path: {image_path} done.")
