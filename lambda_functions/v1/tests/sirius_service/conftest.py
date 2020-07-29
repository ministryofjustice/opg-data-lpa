import pytest

from lambda_functions.v1.functions.lpa.app.api import sirius_service


@pytest.fixture(autouse=False, scope="function")
def patched_get_secret(monkeypatch):
    def mock_secret(*args, **kwargs):
        print("patched_get_secret returning mock_secret")
        return "this_is_a_secret_string"

    monkeypatch.setattr(sirius_service, "get_secret", mock_secret)
