import shutil
from unittest.mock import MagicMock, PropertyMock

import pytest

from owan.domain import IoHandler


class TestIoHandler:
    @pytest.fixture
    def io_handler_factory(self):
        def f():
            return IoHandler()

        return f

    def test_save_upload_file(
        self, io_handler_factory, input_store_path_factory, binary_image_factory
    ):
        io_handler = io_handler_factory()

        input_store_path = input_store_path_factory()
        if input_store_path.exists():
            shutil.rmtree(input_store_path)

        filename = "test_image.png"
        job_id = "job-id"
        dt_string = "dt-string"
        mock_upload_file = MagicMock()
        type(mock_upload_file).file = PropertyMock(return_value=binary_image_factory())
        type(mock_upload_file).filename = PropertyMock(return_value=filename)
        io_handler.save_upload_file(
            mock_upload_file, input_store_path, job_id, dt_string
        )

        excepted_path = input_store_path / f"{dt_string}_{job_id}_{filename}"
        assert excepted_path.exists()
        shutil.rmtree(input_store_path)

    def test_validate_image(self, io_handler_factory, image_path_factory):
        io_handler = io_handler_factory()

        image_path = image_path_factory()
        assert io_handler.validate_image(image_path) is None

    def test_validate_image_invalid(
        self, io_handler_factory, invalid_image_path_factory
    ):
        io_handler = io_handler_factory()

        invalid_image_path = invalid_image_path_factory()
        with pytest.raises(ValueError):
            io_handler.validate_image(invalid_image_path)

    def test_validate_image_unsupported(
        self, io_handler_factory, unsupported_image_path_factory
    ):
        io_handler = io_handler_factory()

        unsupported_image_path = unsupported_image_path_factory()
        with pytest.raises(ValueError):
            io_handler.validate_image(unsupported_image_path)
