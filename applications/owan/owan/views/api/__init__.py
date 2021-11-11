import functools
import logging
import pathlib
import sys
from typing import Iterator

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

import fastapi
from fastapi.responses import JSONResponse

import owan.bootstrap
import owan.domain
import owan.settings
from owan.views.api._lib import (
    _generate_job_id,
    _get_datetime_now_string,
    _predict_preprocess,
)

logger: Final = logging.getLogger("uvicorn")


@functools.lru_cache()
def get_settings() -> owan.settings.Settings:
    return owan.settings.settings()


def _domain_factory(
    settings: owan.settings.Settings = fastapi.Depends(get_settings),
) -> Iterator[owan.domain.Domain]:
    with owan.bootstrap.domain(settings) as domain:
        yield domain


async def predict(
    file: fastapi.UploadFile = fastapi.File(
        ...,
        description="An image file to request. Supported extentions are `.png, .jpeg`.",
    ),
    domain: owan.domain.Domain = fastapi.Depends(_domain_factory),
    settings: owan.settings.Settings = fastapi.Depends(get_settings),
) -> JSONResponse:
    """

    Endpoint for prediction request.

    Raises:

    - **Bad Request (400)**: `file` has unsupported extentions or is invalid as image.

    Example Usage:

    ```
    $ curl -X 'POST' 'http://${IP}:${PORT}/predict' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=./sample_image.png;type=image/png'
    ```

    """
    logger.info(f"predict is called with file: {file.filename}.")
    job_id: Final = _generate_job_id()
    dt_string: Final = _get_datetime_now_string()

    _predict_preprocess(file, domain, settings, job_id, dt_string)
    domain.task_queue.predict()
    return JSONResponse({"recieved_file": f"{file.filename}"})


async def test_predict(
    file: fastapi.UploadFile = fastapi.File(
        ...,
        description="An image file to request. Supported extentions are `.png, .jpeg`.",
    ),
    domain: owan.domain.Domain = fastapi.Depends(_domain_factory),
    settings: owan.settings.Settings = fastapi.Depends(get_settings),
) -> JSONResponse:
    """

    Endpoint for testing prediction request.

    Raises:

    - **Bad Request (400)**: `file` has unsupported extentions or is invalid as image.

    """
    logger.info(f"test_predict is called with file: {file.filename}.")
    job_id: Final = _generate_job_id()
    dt_string: Final = _get_datetime_now_string()

    _predict_preprocess(file, domain, settings, job_id, dt_string)
    domain.task_queue.test_predict(str(pathlib.Path(file.filename)))
    return JSONResponse({"recieved_file": f"{file.filename}"})


async def health() -> JSONResponse:
    """Endpoint for health check."""
    logger.info("health is called.")
    return JSONResponse({"health": "ok"})
