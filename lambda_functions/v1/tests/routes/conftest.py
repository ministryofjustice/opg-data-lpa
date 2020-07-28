import pytest
from flask import Flask

from lambda_functions.v1.functions.lpa.app import create_app


@pytest.fixture(scope="session")
def app(*args, **kwargs):
    app = create_app(Flask)

    routes = [str(p) for p in app.url_map.iter_rules()]
    print(f"routes: {routes}")

    yield app


@pytest.fixture(scope="function")
def test_server(app):
    return app.test_client()
