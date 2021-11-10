import imghdr
import logging
import pathlib
import shutil
import sys
from typing import Set

from starlette.datastructures import UploadFile

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

logger: Final = logging.getLogger("uvicorn")


class IoHandler:
    def __init__(self) -> None:
        pass

    def check_extension(
        self, filepath: pathlib.Path, supported: Set[str] = {".png", ".jpg", ".jpeg"}
    ) -> None:
        """Validate input filepth's extention.

        Args:
            filepath (pathlib.Path): A path to target file including extention.
            supported (Set[str]): A set of supported extentions.

        Raises:
            ValueError: If `filepath` has unsupported extention.

        """
        if filepath.suffix not in supported:
            message: Final = f"extension `{filepath.suffix}` is not supported."
            logger.error(message)
            raise ValueError(message)

    def save_upload_file(
        self,
        file: UploadFile,
        save_dir_path: pathlib.Path,
        job_id: str,
        dt_string: str,
    ) -> pathlib.Path:
        """Save `file` under `save_dir_path`.

        Args:
            file (UploadFile): A file want to save.
            save_dir_path (pathlib.Path): A path to directory where file will be saved.
            job_id (str): A job id. This will used part of filename.
            dt_string (str): A datetime info. This will used part of filename.

        Return:
            pathlib.Path: A path where file is saved.

        """
        if not save_dir_path.exists():
            save_dir_path.mkdir(parents=True, exist_ok=True)

        save_path: Final = save_dir_path / f"{dt_string}_{job_id}_{file.filename}"

        try:
            with save_path.open("wb") as f:
                shutil.copyfileobj(file.file, f)
        finally:
            file.file.close()

        return save_path

    def validate_image(
        self, filepath: pathlib.Path, supported: Set[str] = {".png", ".jpg", ".jpeg"}
    ) -> None:
        """Save `file` under `save_dir_path`.

        Args:
            filepath (pathlib.Path): A path to target image.
            supported (Set[str]): A set of supported extentions.

        Raises:
            ValueError: If image `filepath` is invalid or unsupported.

        """
        image_type: Final = imghdr.what(str(filepath))
        if image_type is None:
            message_invalid: Final = f"file `{str(filepath.name)}` seems to be invalid."
            logger.error(message_invalid)
            raise ValueError(message_invalid)

        extention: Final = "." + image_type
        if extention not in supported:
            message_unsupported: Final = (
                f"file `{str(filepath.name)}` has unsupported data type `{image_type}`."
            )
            logger.error(message_unsupported)
            raise ValueError(message_unsupported)
