import datetime
import pathlib
import sys
import uuid

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

import fastapi
from fastapi import HTTPException

import owan.domain


def _generate_job_id() -> str:
    return str(uuid.uuid4())


def _get_datetime_now_string() -> str:
    format: Final = "%Y:%m:%d-%H:%M:%S"
    diff_jst_from_utc: Final = 9
    now: Final = datetime.datetime.utcnow() + datetime.timedelta(
        hours=diff_jst_from_utc
    )
    return now.strftime(format)


def _predict_preprocess(
    file: fastapi.UploadFile,
    domain: owan.domain.Domain,
    settings: owan.settings.Settings,
    job_id: str,
    dt_string: str,
) -> None:
    """Preprocess of prediction.

    This function does following three things:
    (1) Validate `file`'s extention.
    (2) Save `file` temporally.
    (3) Check if saved `file` is valid image.

    """
    # Validate extention.
    try:
        domain.io.check_extension(
            pathlib.Path(file.filename),
            settings.io.input_supported_extensions,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=getattr(e, "message", str(e)))

    # Save file temporally.
    try:
        save_path = domain.io.save_upload_file(
            file, settings.input_store.path, job_id, dt_string
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=getattr(e, "message", str(e)))

    # Check if saved file is valid image.
    try:
        domain.io.validate_image(save_path, settings.io.input_supported_extensions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=getattr(e, "message", str(e)))
