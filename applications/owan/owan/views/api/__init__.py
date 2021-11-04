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
    generate_job_id,
    get_datetime_now_string,
    save_upload_file,
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
    file: fastapi.UploadFile = fastapi.File(...),
    domain: owan.domain.Domain = fastapi.Depends(_domain_factory),
) -> JSONResponse:

    domain.task_queue.predict()
    return fastapi.responses.JSONResponse({})


async def test_predict(
    file: fastapi.UploadFile = fastapi.File(...),
    domain: owan.domain.Domain = fastapi.Depends(_domain_factory),
    settings: owan.settings.Settings = fastapi.Depends(get_settings),
) -> JSONResponse:
    logger.info(f"test_predict is called with file: {file.filename}.")
    save_upload_file(
        file, settings.input_store.path, generate_job_id(), get_datetime_now_string()
    )
    domain.task_queue.test_predict(str(pathlib.Path(file.filename)))
    return fastapi.responses.JSONResponse({})


async def health() -> JSONResponse:
    """Endpoint for health check."""
    logger.info("health is called.")
    return JSONResponse({"health": "ok"})
