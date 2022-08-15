from unittest import mock

import pytest
from receipt_service.clients.api_client import APIClient, BearerAuth, RequestContext
from receipt_service.clients.request_client import NoOpClient
from tests.helpers import dict_contains


@pytest.fixture
def request_context():
    return RequestContext(url="123")


@pytest.fixture
def auth():
    return BearerAuth(token="123")


def test_bearer_context_processing(request_context: RequestContext, auth):
    auth.authenticate(request_context)
    assert request_context.headers
    assert "Authorization" in request_context.headers
    assert request_context.headers["Authorization"] == f"Bearer {auth.token}"


def test_bearer_context_with_headers_processing(request_context: RequestContext, auth):
    request_context.headers = {"a": "b"}
    auth.authenticate(request_context)
    assert request_context.headers
    assert "Authorization" in request_context.headers
    assert request_context.headers["Authorization"] == f"Bearer {auth.token}"
    assert request_context.headers["a"] == "b"


def test_bearer_auth():
    class FakeAPI(APIClient):
        methods = ['get']
        auth = BearerAuth(token="123")
        network_client = mock.create_autospec(NoOpClient)
        base_url: str = "http://test.com"
        endpoints = ["test"]

    api = FakeAPI()
    api.network_client.get.return_value = '{}'
    api.get_test()
    assert api.network_client.get.call_args.kwargs['headers'] == dict_contains({'Authorization': 'Bearer 123'})
