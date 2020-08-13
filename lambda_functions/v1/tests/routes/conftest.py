from textwrap import wrap

import fakeredis
import pytest
from flask import Flask

from lambda_functions.v1.functions.lpa.app import create_app
from lambda_functions.v1.functions.lpa.app.config import LocalTestingConfig

from lambda_functions.v1.functions.lpa.app.sirius_service import sirius_handler
from lambda_functions.v1.tests.helpers import load_data

mock_redis_server = fakeredis.FakeServer()


class NoCache(LocalTestingConfig):
    REQUEST_CACHING = "disabled"


@pytest.fixture(scope="session")
def app(*args, **kwargs):

    app = create_app(Flask, config=LocalTestingConfig)

    routes = [str(p) for p in app.url_map.iter_rules()]
    print(f"routes: {routes}")

    app.sirius.cache = fakeredis.FakeStrictRedis(
        charset="utf-8", decode_responses=True, server=mock_redis_server
    )

    yield app


@pytest.fixture(scope="function")
def test_server(app):

    return app.test_client()


@pytest.fixture(scope="session")
def app_no_cache(*args, **kwargs):
    app = create_app(Flask, config=NoCache)

    routes = [str(p) for p in app.url_map.iter_rules()]
    print(f"routes: {routes}")

    app.sirius.cache = fakeredis.FakeStrictRedis(
        charset="utf-8", decode_responses=True, server=mock_redis_server
    )

    yield app


@pytest.fixture(scope="function")
def test_server_no_cache(app_no_cache):
    return app_no_cache.test_client()


@pytest.fixture(autouse=True)
def patched_get_secret(monkeypatch):
    def mock_secret(*args, **kwargs):
        print("patched_get_secret returning mock_secret")
        return "this_is_a_secret_string"

    monkeypatch.setattr(sirius_handler.SiriusService, "_get_secret", mock_secret)


@pytest.fixture()
def patched_send_request_to_sirius(monkeypatch):
    def mock_get(*args, **kwargs):
        print("Using fake_send_request_to_sirius ")
        print(f"args: {args}")
        print(f"kwargs: {kwargs}")

        url = args[1]

        # test_id = kwargs["url"].split("=")[1]
        test_id = url.split("=")[1]
        print(f"test_id: {test_id}")

        if test_id[0] == "7":
            print(f"test_id is a valid sirius uid: {test_id}")

            response_data = load_data("use_an_lpa_response.json", as_json=False)

            response_data["uid"] = "-".join(wrap(test_id, 4))

            response_data = [response_data]

            return 200, response_data

        elif test_id[0] == "A":
            print(f"test_id is a valid lpa-online-tool id: {test_id}")

            response_data = load_data("lpa_online_tool_response.json", as_json=False)

            response_data["onlineLpaId"] = test_id

            response_data = [response_data]

            return 200, response_data

        elif test_id[:5] == "crash":
            print("oh no you crashed sirius")

            response_code = test_id[-3:]

            return response_code, f"Sirius broke bad - error {response_code}"

        else:
            print("test_id is not a valid sirius_uid or lpa-online-tool id")
            return 404, ""

    monkeypatch.setattr(sirius_handler.SiriusService, "_get_data_from_sirius", mock_get)


@pytest.fixture
def patched_send_request_to_sirius_available(monkeypatch):
    monkeypatch.setattr(
        sirius_handler.SiriusService, "_check_sirius_available", lambda x: True
    )


@pytest.fixture
def patched_send_request_to_sirius_unavailable(monkeypatch):
    monkeypatch.setattr(
        sirius_handler.SiriusService, "_check_sirius_available", lambda x: False
    )
