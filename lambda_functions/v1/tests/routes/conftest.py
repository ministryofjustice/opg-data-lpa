import pytest
from flask import Flask

from lambda_functions.v1.functions.lpa.app import create_app
from lambda_functions.v1.functions.lpa.app.api import sirius_service


@pytest.fixture(scope="session")
def app(*args, **kwargs):
    app = create_app(Flask)

    routes = [str(p) for p in app.url_map.iter_rules()]
    print(f"routes: {routes}")

    yield app


@pytest.fixture(scope="function")
def test_server(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def patched_get_secret(monkeypatch):
    def mock_secret(*args, **kwargs):
        print("patched_get_secret returning mock_secret")
        return "this_is_a_secret_string"

    monkeypatch.setattr(sirius_service, "get_secret", mock_secret)
