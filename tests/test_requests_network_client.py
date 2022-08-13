

from unittest.mock import patch
from receipt_service.clients.request_client import RequestClient


@patch('requests.get')
def test_get_method(mock_get):
    RequestClient.get(None, None, None)
    mock_get.assert_called_once()


@patch('requests.post')
def test_post_method(mock_post):
    RequestClient.post(None, None, None)
    mock_post.assert_called_once()


@patch('requests.get')
def test_get_method_arguments(mock_get):
    RequestClient.get("1", "2", "3")
    mock_get.assert_called_once_with('1', params='2', data='3')


@patch('requests.post')
def test_post_method_arguments(mock_post):
    RequestClient.post("1", "2", "3")
    mock_post.assert_called_once_with('1', params='2', data='3')
