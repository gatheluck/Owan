import functools
from typing import Iterator

import fastapi
from fastapi.responses import JSONResponse

import owan.bootstrap
import owan.domain
import owan.settings


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


async def health() -> JSONResponse:
    """Endpoint for health check."""
    return JSONResponse({"health": "ok"})
