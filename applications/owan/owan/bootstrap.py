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


def domain_factory(settings: owan.settings.Settings) -> owan.domain.Domain:
    broker: Final = owan.tasks.Factory(broker=settings.redis.dns).broker
    return owan.domain.Domain(broker=broker)


@contextlib.contextmanager
def domain(settings: owan.settings.Settings) -> Iterator[owan.domain.Domain]:
    yield owan.bootstrap.domain_factory(settings)
