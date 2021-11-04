import pathlib

import pytest

test_input_path = pathlib.Path("./tests/samples/sample_input_01.png")
test_input_store_path = pathlib.Path("./tests/tmp/input_store")


@pytest.fixture
def image_path_factory():
    def f(image_path=test_input_path):
        return image_path

    return f


@pytest.fixture
def input_store_path_factory():
    def f(input_store_path=test_input_store_path):
        return input_store_path

    return f


@pytest.fixture
def binary_image_factory():
    def f(image_path=test_input_path):
        return image_path.open("rb")

    return f
