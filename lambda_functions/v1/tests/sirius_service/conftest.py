import pytest


import os


# Defaults to 50
import requests

from lambda_functions.v1.functions.lpa.app.api import sirius_service
import os


# Defaults to 50
max_examples = int(os.environ["HYPOTHESIS_MAX_EXAMPLES"])

max_examples = int(os.environ["HYPOTHESIS_MAX_EXAMPLES"])


@pytest.fixture()
def patched_get_secret(monkeypatch):
    def mock_secret(*args, **kwargs):
        print("patched_get_secret returning mock_secret")
        return "this_is_a_secret_string"

    monkeypatch.setattr(sirius_service, "get_secret", mock_secret)


@pytest.fixture()
def patched_build_sirius_headers(monkeypatch):
    def mock_headers(*args, **kwargs):

        return {
            "Content-Type": args[0] if args[0] else "application/json",
            "Authorization": "Bearer not-a-real-token",
        }

    monkeypatch.setattr(sirius_service, "build_sirius_headers", mock_headers)


@pytest.fixture()
def patched_requests(monkeypatch):
    def mock_get(*args, **kwargs):
        print("mock GET")

        mock_response = requests.Response()
        mock_response.status_code = 200

        def json_func():
            payload = {
                "request_type": "get",
                "headers": kwargs["headers"] if "headers" in kwargs else None,
                "data": kwargs["data"] if "data" in kwargs else None,
            }
            return payload

        mock_response.json = json_func

        return mock_response

    def mock_post(*args, **kwargs):
        print("mock POST")
        mock_response = requests.Response()
        mock_response.status_code = 200

        def json_func():
            payload = {
                "request_type": "post",
                "headers": kwargs["headers"] if "headers" in kwargs else None,
                "data": kwargs["data"] if "data" in kwargs else None,
            }
            return payload

        mock_response.json = json_func

        return mock_response

    def mock_put(*args, **kwargs):
        print("mock PUT")
        mock_response = requests.Response()
        mock_response.status_code = 200

        def json_func():
            payload = {
                "request_type": "put",
                "headers": kwargs["headers"] if "headers" in kwargs else None,
                "data": kwargs["data"] if "data" in kwargs else None,
            }
            return payload

        mock_response.json = json_func

        return mock_response

    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "put", mock_put)


@pytest.fixture()
def patched_requests_broken(monkeypatch):
    def mock_broken_get(*args, **kwargs):
        print("mock broken GET")

        return None

    monkeypatch.setattr(requests, "get", mock_broken_get)
