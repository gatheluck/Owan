import http
import unittest.mock

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


def test_predict(dummy_client, binary_image_factory):
    mock_domain = unittest.mock.MagicMock()
    client = dummy_client(mock_domain)
    files = {"file": binary_image_factory()}

    response = client.post("/predict", files=files)
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == {}
    mock_domain.task_queue.predict.assert_called_once_with()


def test_health(dummy_client):
    mock_domain = unittest.mock.MagicMock()
    client = dummy_client(mock_domain)

    response = client.get("/health")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == {"health": "ok"}
