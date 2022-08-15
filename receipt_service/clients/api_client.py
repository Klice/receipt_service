import copy
from dataclasses import asdict, dataclass
import json
import re
from typing import Any

from receipt_service.clients.request_client import RequestClient


class APIClient:
    auth = None
    base_url: str = None
    headers = None
    network_client = RequestClient
    def response_parser(self, x): return json.loads(x)
    endpoints = None
    methods = ['post', 'get', 'put']
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    def __init__(self, network_client=None):
        if network_client:
            self.network_client = network_client
        if self.endpoints:
            self._build_api_methods()

    def _build_api_methods(self):
        for e in self.endpoints:
            self._create_methods(e)

    def _create_methods(self, endpoint):
        for method in self.methods:
            method_name = self._get_method_name(method, endpoint)
            api_method = self._get_method_implementation(method, endpoint)
            api_method.__doc__ = f"docstring for api_method {method_name}"
            api_method.__name__ = method_name
            setattr(self, api_method.__name__, api_method)

    @classmethod
    def _get_method_name(cls, method, endpoint):
        endpoint = cls._remove_parameters(endpoint)
        endpoint = cls._camel_to_snake(endpoint)
        return f"{method}_{endpoint}"

    @staticmethod
    def _remove_parameters(endpoint):
        return re.sub(r"[{}]", "", endpoint)

    @staticmethod
    def _camel_to_snake(name) -> str:
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', name)
        return '_'.join(map(str.lower, words))

    def _get_method_implementation(self, method, endpoint):
        def api_method(params=None, data=None, headers=None, **kwargs):
            if self.headers:
                req_headers = copy.deepcopy(self.headers)
                if headers:
                    req_headers.update(headers)
            else:
                req_headers = headers

            context = RequestContext(
                url=f"{self.base_url}/{endpoint.format(**kwargs)}",
                params=params,
                data=data,
                headers=req_headers,
            )
            if self.auth:
                self.auth.authenticate(context)
            res = getattr(self.network_client, method)(**asdict(context))
            if self.response_parser:
                return self.response_parser(res)
            return res
        return api_method


@dataclass
class RequestContext:
    url: str
    params: dict = None
    data: Any = None
    headers: Any = None


class BearerAuth:
    token = None

    def __init__(self, token):
        self.token = token

    def authenticate(self, context: RequestContext):
        res = {'Authorization': f"Bearer {self.token}"}
        if context.headers:
            context.headers.update(res)
        else:
            context.headers = res
