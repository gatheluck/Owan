import pathlib

import pytest


@pytest.fixture
def binary_image_factory():
    def f(imagepath=pathlib.Path("./tests/samples/sample_input_01.png")):
        return imagepath.open("rb")

    return f
