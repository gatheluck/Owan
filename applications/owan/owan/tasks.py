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

logger: Final = logging.getLogger("uvicorn")


def _predict() -> None:
    with owan.bootstrap.domain(owan.settings.settings()) as domain:
        domain.task_worker.predict()


def _test_predict(image_path: str) -> None:
    with owan.bootstrap.domain(owan.settings.settings()) as domain:
        domain.task_worker.test_predict(image_path, domain.storage)


class TaskQueue:
    """Provide method which is executable through task queue."""

    def __init__(self, celeryapp: celery.Celery) -> None:
        self._predict: Final = celeryapp.task(_predict)
        self._test_predict: Final = celeryapp.task(_test_predict)

    def predict(self) -> celery.result.AsyncResult:
        """Wrapper of Celery task. Execute prediction."""
        return self._predict.delay()

    def test_predict(self, image_path: str) -> celery.result.AsyncResult:
        """Wrapper of Celery task. Execute test prediction."""
        logger.info("Enqueue test_predict.")
        return self._test_predict.delay(image_path)


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
