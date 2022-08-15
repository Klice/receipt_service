

from unittest.mock import patch

import pytest

from receipt_service.clients.request_client import RequestClient


@pytest.mark.parametrize("method", [
    "get",
    "post",
    "put",
    "delete"
])
def test_get_methods_exist(method):
    with patch(f"requests.{method}") as mock_method:
        getattr(RequestClient, method)("1", "2", "3", headers={"a": "b"})
        mock_method.assert_called_once_with('1', params='2', data='3', headers={"a": "b"})
