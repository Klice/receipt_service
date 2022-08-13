from unittest.mock import Mock

import pytest

from receipt_service.clients.api_client import APIClient


def test_api_client():
    mock_client = Mock()
    c = APIClient(network_client=mock_client)
    assert c.network_client == mock_client


@pytest.fixture
def fake_api():
    class FakeAPI(APIClient):
        base_url = "http://fake.com"
        network_client = Mock()
        response_parser = Mock()
        endpoints = [
            "fake_news",
            "sub/fake_news",
        ]
    return FakeAPI()


def test_api_client_generate_methods(fake_api):
    assert is_method_exists(fake_api, "get_fake_news")
    assert is_method_exists(fake_api, "post_fake_news")
    assert is_method_exists(fake_api, "get_sub_fake_news")
    assert is_method_exists(fake_api, "post_sub_fake_news")


def test_api_client_generate_methods_calls(fake_api: APIClient):
    fake_api.get_fake_news(params="1")
    fake_api.post_fake_news(params="1", body="2")
    fake_api.network_client.get.assert_called_once_with(fake_api.base_url, params="1", body=None)
    fake_api.network_client.post.assert_called_once_with(fake_api.base_url, params="1", body="2")
    assert 2 == fake_api.response_parser.call_count


def test_no_response_parser(fake_api: APIClient):
    fake_api.response_parser = None
    fake_api.network_client.get.return_value = "111"
    assert fake_api.get_fake_news(params="1") == "111"


def test_api_client_generate_methods_calls_return(fake_api: APIClient):
    fake_api.response_parser = lambda x: x
    fake_api.network_client.get.return_value = "111"
    fake_api.network_client.post.return_value = "222"
    res1 = fake_api.get_fake_news(params="1")
    res2 = fake_api.post_fake_news(params="1", body="2")
    assert res1 == "111"
    assert res2 == "222"


def is_method_exists(obj, method):
    return hasattr(obj, method) and callable(getattr(obj, method))
