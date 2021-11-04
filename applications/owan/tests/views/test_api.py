import http
import shutil
import unittest.mock
from unittest.mock import MagicMock, PropertyMock

import fastapi
import fastapi.testclient
import pytest

import owan.views.api
import owan.views.routing
from owan.views.api._lib import save_upload_file


def mock_domain_factory_factory(mock_domain=unittest.mock.MagicMock()):
    def f():
        return mock_domain

    return f


@pytest.fixture
def dummy_client():
    def f(mock_domain=unittest.mock.MagicMock()):
        app = fastapi.FastAPI()
        app.dependency_overrides[
            owan.views.api._domain_factory
        ] = mock_domain_factory_factory(mock_domain)
        owan.views.routing.add_routes(app)
        return fastapi.testclient.TestClient(app)

    return f


def test_predict(dummy_client, binary_image_factory):
    mock_domain = unittest.mock.MagicMock()
    client = dummy_client(mock_domain)
    files = {"file": binary_image_factory()}

    response = client.post("/predict", files=files)
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == {}
    mock_domain.task_queue.predict.assert_called_once_with()


def test_health(dummy_client):
    mock_domain = MagicMock()
    client = dummy_client(mock_domain)

    response = client.get("/health")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == {"health": "ok"}


def test_save_upload_file(input_store_path_factory, binary_image_factory):
    input_store_path = input_store_path_factory()
    if input_store_path.exists():
        shutil.rmtree(input_store_path)

    filename = "test_image.png"
    job_id = "job-id"
    dt_string = "dt-string"
    mock_upload_file = MagicMock()
    type(mock_upload_file).file = PropertyMock(return_value=binary_image_factory())
    type(mock_upload_file).filename = PropertyMock(return_value=filename)
    save_upload_file(mock_upload_file, input_store_path, job_id, dt_string)

    excepted_path = input_store_path / f"{dt_string}_{job_id}_{filename}"
    assert excepted_path.exists()
    shutil.rmtree(input_store_path)
