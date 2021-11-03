import logging
import sys

import celery
import celery.result

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

import owan.bootstrap
import owan.settings

logger: Final = logging.Logger(__name__)


def _predict() -> None:
    logger.error("predict is executed form TaskQueue")

    with owan.bootstrap.domain(owan.settings.settings()) as domain:
        domain.task_worker.predict()


class TaskQueue:
    """Provide method which is executable through task queue."""

    def __init__(self, celeryapp: celery.Celery) -> None:
        self._predict: Final = celeryapp.task(_predict)

    def predict(self) -> celery.result.AsyncResult:
        """Wrapper of Celery task. Execute prediction."""
        return self._predict.delay()


class Factory:
    """Generate broker and worker for task queue.

    Broker example usage:
    >>> broker = Factory(broker="redis://...").broker
    >>> broker.just_print.delay("Hello Task Queue")

    Worker example usage:
    >>> app = Factory(broker="redis://...").worker

    """

    def __init__(self, broker: str) -> None:
        self.worker: Final = celery.Celery(broker=broker)
        self.broker: Final = TaskQueue(self.worker)
