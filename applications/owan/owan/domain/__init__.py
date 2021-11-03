import logging
import sys

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

import owan.tasks

logger: Final = logging.Logger(__name__)


class Domain:
    def __init__(
        self,
        broker: owan.tasks.TaskQueue,
    ) -> None:
        self.task_queue: Final = broker
        self.task_worker: Final = _TaskWorker()


class _TaskWorker:
    """TaskWorker subdomain class which execute tasks asked from _TaskQueue"""

    def __init__(self) -> None:
        pass

    def predict(self) -> None:
        logger.error("predict from _TaskWorker")
