"""
Entry point module for celery worker.
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

import owan.settings
import owan.tasks

settings: Final = owan.settings.settings()
app: Final = owan.tasks.Factory(broker=settings.redis.dns).worker
