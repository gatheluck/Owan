import pathlib

import pytest

input_path = pathlib.Path("./tests/samples/valid_input_01.png")
invalid_input_path = pathlib.Path("./tests/samples/invalid_input_01.png")
unsupported_input_path = pathlib.Path("./tests/samples/unsupported_input_01.png")
input_store_path = pathlib.Path("./tests/tmp/input_store")


@pytest.fixture
def image_path_factory():
    def f(image_path=input_path):
        return image_path

    return f


@pytest.fixture
def invalid_image_path_factory():
    def f(image_path=invalid_input_path):
        return image_path

    return f


@pytest.fixture
def unsupported_image_path_factory():
    def f(image_path=unsupported_input_path):
        return image_path

    return f


@pytest.fixture
def input_store_path_factory():
    def f(input_store_path=input_store_path):
        return input_store_path

    return f


@pytest.fixture
def binary_image_factory():
    def f(image_path=input_path):
        return image_path.open("rb")

    return f
