import http
import unittest.mock
from unittest.mock import MagicMock

import fastapi
import fastapi.testclient
import pytest

import owan.views.api
import owan.views.routing


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


def test_predict(dummy_client, binary_image_factory, image_path_factory):
    mock_domain = unittest.mock.MagicMock()
    client = dummy_client(mock_domain)
    files = {"file": binary_image_factory()}
    expected = {"recieved_file": str(image_path_factory().name)}

    response = client.post("/predict", files=files)
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == expected
    mock_domain.task_queue.predict.assert_called_once()


def test_test_predict(dummy_client, binary_image_factory, image_path_factory):
    mock_domain = unittest.mock.MagicMock()
    client = dummy_client(mock_domain)
    files = {"file": binary_image_factory()}
    expected_response = {"recieved_file": str(image_path_factory().name)}

    response = client.post("/predict/test", files=files)
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == expected_response
    mock_domain.task_queue.test_predict.assert_called_once()


def test_health(dummy_client):
    mock_domain = MagicMock()
    client = dummy_client(mock_domain)

    response = client.get("/health")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == {"health": "ok"}
