import json
from unittest import mock
from unittest.mock import ANY, Mock

import pytest

from receipt_service.clients.api_client import APIClient, RequestContext
from receipt_service.clients.request_client import NoOpClient
from tests.helpers import dict_contains, is_method_exists


def test_api_client():
    mock_client = Mock()
    c = APIClient(network_client=mock_client)
    assert c.network_client == mock_client


@pytest.fixture
def fake_api():
    class FakeAPI(APIClient):
        base_url = "http://fake.com"
        network_client = mock.create_autospec(NoOpClient)
        response_processor = Mock()
        request_processor = Mock(side_effect=lambda x: x)
        endpoints = [
            "fake_news",
            "sub/fake_news",
            "fake_news/{news_id}",
        ]
    return FakeAPI()


def test_incorrect_args(fake_api):
    with pytest.raises(TypeError):
        fake_api.network_client.get(b="1")


@pytest.mark.parametrize("endpoint", [
    "fake_news",
    "sub_fake_news"
])
def test_api_client_generate_methods(fake_api, endpoint):
    assert is_method_exists(fake_api, f"get_{endpoint}")
    assert is_method_exists(fake_api, f"post_{endpoint}")
    assert is_method_exists(fake_api, f"put_{endpoint}")
    assert is_method_exists(fake_api, f"delete_{endpoint}")


def test_api_client_generate_methods_calls(fake_api: APIClient):
    fake_api.get_fake_news(params="1")
    fake_api.post_fake_news(params="1", data="2")
    fake_api.get_sub_fake_news(params="1")

    fake_api.network_client.get.assert_any_call(fake_api.base_url+"/fake_news", params="1", data=None, headers=ANY)
    fake_api.network_client.get.assert_any_call(fake_api.base_url+"/sub/fake_news", params="1", data=None, headers=ANY)
    fake_api.network_client.post.assert_called_once_with(
        fake_api.base_url+"/fake_news", params="1", data="2", headers=fake_api.headers
    )
    assert 3 == fake_api.response_processor.call_count


def test_api_client_headers(fake_api: APIClient):
    fake_api.get_fake_news(headers={"a": "b"})
    fake_api.network_client.get.assert_any_call(
        fake_api.base_url+"/fake_news", headers=dict_contains({"a": "b"}), params=None, data=None
    )


def test_no_request_processor(fake_api: APIClient):
    fake_api.request_processor = None
    fake_api.get_fake_news(params="321", data="ddd")
    fake_api.network_client.get.assert_any_call(fake_api.base_url+"/fake_news", params="321", data="ddd", headers=ANY)


def test_json_request_processor(fake_api: APIClient):
    def processor(r: RequestContext):
        r.data = json.dumps(r.data)
        return r
    fake_api.request_processor = processor
    fake_api.get_fake_news(params="321", data={"a": "b"})
    fake_api.network_client.get.assert_any_call(
        fake_api.base_url+"/fake_news", params="321", data='{"a": "b"}', headers=ANY
    )


def test_no_response_processor(fake_api: APIClient):
    fake_api.response_processor = None
    fake_api.network_client.get.return_value = "111"
    assert fake_api.get_fake_news(params="1") == "111"


def test_api_client_generate_methods_calls_return(fake_api: APIClient):
    fake_api.response_processor = lambda x: x
    fake_api.network_client.get.return_value = "111"
    fake_api.network_client.post.return_value = "222"
    res1 = fake_api.get_fake_news(params="1")
    res2 = fake_api.post_fake_news(params="1", data="2")
    assert res1 == "111"
    assert res2 == "222"


def test_api_client_parametrized(fake_api: APIClient):
    assert is_method_exists(fake_api, "get_fake_news_news_id")
    fake_api.get_fake_news_news_id(news_id="ttt")
    assert fake_api.network_client.get.call_args.kwargs["url"] == 'http://fake.com/fake_news/ttt'


def test_auth(fake_api: APIClient):
    fake_api.network_client.get.return_value = "111"
    fake_api.auth = Mock()
    fake_api.network_client.post.return_value = "111"
    fake_api.post_fake_news(params="1", data="2", headers={"a": "3"})
    fake_api.auth.authenticate.assert_called_once_with(
        RequestContext(fake_api.base_url+"/fake_news", params="1", data="2", headers=dict_contains({"a": "3"}))
    )


def test_headers(fake_api: APIClient):
    fake_api.headers = {"a": "b"}
    fake_api.network_client.get.return_value = "111"
    fake_api.get_fake_news(params="1", data="2")
    assert fake_api.network_client.get.call_args.kwargs["headers"] == {"a": "b"}
