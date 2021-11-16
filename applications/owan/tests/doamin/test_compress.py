import shutil
import unittest

import pytest

from owan.domain.compress import Compressor


class TestCompressor:
    @pytest.fixture
    def compressor_factory(self):
        def f(
            input_supported_extention=unittest.mock.MagicMock(),
            compress_quality=unittest.mock.MagicMock(),
        ):
            return Compressor(
                input_supported_extention=input_supported_extention,
                compress_quality=compress_quality,
            )

        return f

    def test_compress_image(
        self, compressor_factory, image_path_factory, output_image_path_factory
    ):
        compressor = compressor_factory({".png", ".jpeg"}, 30)

        input_path = image_path_factory()
        output_path = output_image_path_factory()
        assert not output_path.exists()
        compressor.compress_image(input_path, output_path)

        excepted_path = output_path
        assert excepted_path.exists()
        shutil.rmtree(excepted_path.parent)

    def test_compress_image_invalid_extention(
        self, compressor_factory, image_path_factory, output_image_path_factory
    ):
        compressor = compressor_factory({""}, 30)

        input_path = image_path_factory()
        output_path = output_image_path_factory()
        assert not output_path.exists()
        with pytest.raises(ValueError):
            compressor.compress_image(input_path, output_path)

    def test_compress_image_invalid_input(
        self, compressor_factory, invalid_image_path_factory, output_image_path_factory
    ):
        compressor = compressor_factory({""}, 30)

        input_path = invalid_image_path_factory()
        output_path = output_image_path_factory()
        assert not output_path.exists()
        with pytest.raises(ValueError):
            compressor.compress_image(input_path, output_path)
