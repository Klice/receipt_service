import requests


class RequestClient:
    @classmethod
    def get(cls, url, params, data):
        requests.get(url, params=params, data=data)

    @classmethod
    def post(cls, url, params, data):
        requests.post(url, params=params, data=data)
