import unittest.mock

import pytest

import owan.domain


class TestTaskQueue:
    @pytest.fixture
    def domain_factory(self):
        def f(broker=unittest.mock.MagicMock()):
            return owan.domain.Domain(broker=broker)

        return f

    def test_test_predict(self, domain_factory, image_path_factory):

        mock_broker = unittest.mock.MagicMock()
        domain = domain_factory(broker=mock_broker)
        domain.task_queue.test_predict(image_path_factory())
        mock_broker.test_predict.assert_called_once()
