import logging
import pathlib
import sys
from io import BytesIO
from typing import Set

from PIL import Image

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

logger: Final = logging.getLogger("uvicorn")


class Compressor:
    def __init__(
        self, input_supported_extention: Set[str], compress_quality: int
    ) -> None:
        self.input_supported_extention: Final = input_supported_extention
        self.compress_quality: Final = compress_quality

    def compress_image(
        self,
        input_path: pathlib.Path,
        output_path: pathlib.Path,
    ) -> None:
        """Compress input image and save as jpeg image.

        Args:
            input_path (pathlib.Path): A path of input image.
            output_path (pathlib.Path): A path of output image.

        Raises:
            ValueError: If `input_path` has unsupported extention
                        or `output_path` is not jpeg file.

        """
        extention: Final = input_path.suffix
        if extention not in self.input_supported_extention:
            message = f"extension `{extention}` is not supported."
            logger.error(message)
            raise ValueError(message)

        if output_path.suffix != ".jpeg":
            message = "output extension should be `.jpeg`."
            logger.error(message)
            raise ValueError(message)

        with input_path.open(mode="rb") as f:
            im: Final = (
                Image.open(f).convert("RGB") if extention == ".png" else Image.open(f)
            )
            im_io = BytesIO()
            im.save(im_io, "JPEG", quality=self.compress_quality)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open(mode="wb") as f:
            f.write(im_io.getvalue())
