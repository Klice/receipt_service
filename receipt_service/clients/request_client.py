import requests


class RequestClient:
    @classmethod
    def get(cls, url, params, data, headers):
        return requests.get(url, params=params, data=data, headers=headers).text

    @classmethod
    def post(cls, url, params, data, headers):
        return requests.post(url, params=params, data=data, headers=headers).text

    @classmethod
    def put(cls, url, params, data, headers):
        res = requests.put(url, params=params, data=data, headers=headers)
        return res.text

    @classmethod
    def delete(cls, url, params, data, headers):
        return requests.delete(url, params=params, data=data, headers=headers).text


class NoOpClient:
    @classmethod
    def get(cls, url, params, data, headers):
        pass

    @classmethod
    def post(cls, url, params, data, headers):
        pass

    @classmethod
    def put(cls, url, params, data, headers):
        pass

    @classmethod
    def delete(cls, url, params, data, headers):
        pass
