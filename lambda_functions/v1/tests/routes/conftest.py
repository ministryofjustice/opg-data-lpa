from textwrap import wrap

import atexit
import fakeredis
import pytest
from flask import Flask

from lambda_functions.v1.functions.lpa.app import create_app
from lambda_functions.v1.functions.lpa.app.config import LocalTestingConfig

from opg_sirius_service import sirius_handler
from lambda_functions.v1.tests.helpers import load_data
from pact import Consumer, Provider

mock_redis_server = fakeredis.FakeServer()


class NoCache(LocalTestingConfig):
    REQUEST_CACHING = "disabled"


@pytest.fixture(scope="session")
def app(*args, **kwargs):
    app = create_app(Flask, config=LocalTestingConfig)

    routes = [str(p) for p in app.url_map.iter_rules()]
    print(f"routes: {routes}")

    app.sirius.cache = fakeredis.FakeStrictRedis(
        encoding="utf-8", decode_responses=True, server=mock_redis_server
    )

    yield app


@pytest.fixture(scope="function")
def cache(app):
    return app.sirius.cache


@pytest.fixture(scope="session")
def test_server(app):
    return app.test_client()


@pytest.fixture(scope="session")
def app_no_cache(*args, **kwargs):
    app = create_app(Flask, config=NoCache)

    routes = [str(p) for p in app.url_map.iter_rules()]
    print(f"routes: {routes}")

    app.sirius.cache = fakeredis.FakeStrictRedis(
        encoding="utf-8", decode_responses=True, server=mock_redis_server
    )

    yield app


@pytest.fixture(scope="session")
def mock_environ():
    environ = {
        "SOURCE_IP": "127.0.0.1",
        "USER_AGENT": "Mock User Agent",
        "REQUEST_METHOD": "GET",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "PATH_INFO": "/example",
        "REQUEST_ID": "123456789",
    }
    return environ


@pytest.fixture(scope="session")
def pact():
    pact = Consumer("data-lpa").has_pact_with(Provider("sirius"), pact_dir="/tmp/pact")
    pact.start_service()
    atexit.register(pact.stop_service)

    return pact


@pytest.fixture(scope="session")
def test_server_pact(pact):
    app = create_app(Flask, config=LocalTestingConfig)

    app.sirius.sirius_base_url = pact.uri
    app.sirius.cache = fakeredis.FakeStrictRedis(
        encoding="utf-8", decode_responses=True, server=mock_redis_server
    )

    return app.test_client()


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

        if (
            args[2] == "POST"
            and url == "http://not-really-sirius.com/api/public/v1/lpas/requestCode"
        ):
            return 204, ""

        # test_id = kwargs["url"].split("=")[1]
        test_id = url.split("=")[1]
        print(f"test_id: {test_id}")

        if test_id[0] == "7":
            print(f"test_id is a valid sirius uid: {test_id}")

            successful_response_data = load_data(
                "use_an_lpa_successful_response.json", as_json=False
            )

            successful_response_data["uid"] = "-".join(wrap(test_id, 4))

            response_data = [successful_response_data]

            return 200, response_data

        elif test_id[0] == "A":
            print(f"test_id is a valid lpa-online-tool id: {test_id}")

            successful_response_data = load_data(
                "lpa_online_tool_successful_response.json", as_json=False
            )

            for lpa in successful_response_data["lpa"]:
                if test_id in lpa["onlineLpaId"]:
                    response_data = [lpa]

                    return 200, response_data

            deleted_response_data = load_data(
                "lpa_online_tool_deleted_response.json", as_json=False
            )

            for lpa in deleted_response_data["lpa"]:
                if test_id in lpa["onlineLpaId"]:
                    return 410, {
                        "detail": "LPA with uid " + test_id + "has been deleted"
                    }

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
        sirius_handler.SiriusService, "check_sirius_available", lambda x: True
    )


@pytest.fixture
def patched_send_request_to_sirius_unavailable(monkeypatch):
    monkeypatch.setattr(
        sirius_handler.SiriusService, "check_sirius_available", lambda x: False
    )
