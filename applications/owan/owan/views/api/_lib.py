import datetime
import pathlib
import shutil
import sys
import uuid

from starlette.datastructures import UploadFile

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final


def generate_job_id() -> str:
    return str(uuid.uuid4())


def get_datetime_now_string() -> str:
    format: Final = "%Y:%m:%d-%H:%M:%S"
    return datetime.datetime.now().strftime(format)


def save_upload_file(
    file: UploadFile,
    save_dir_path: pathlib.Path,
    job_id: str,
    dt_string: str,
) -> None:
    if not save_dir_path.exists():
        save_dir_path.mkdir(parents=True, exist_ok=True)

    save_path: Final = save_dir_path / f"{dt_string}_{job_id}_{file.filename}"

    try:
        with save_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)
    finally:
        file.file.close()
