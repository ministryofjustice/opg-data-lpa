from lambda_functions.v1.functions.lpa.app.api.sirius_service import (
    check_sirius_available,
)
import pytest
import requests


@pytest.fixture
def patched_sirius_heathcheck(monkeypatch):
    def mock_healthcheck(*args, **kwargs):
        mock_response = requests.Response()
        mock_response.status_code = 200

        return mock_response

    monkeypatch.setattr(requests, "get", mock_healthcheck)


@pytest.fixture
def patched_sirius_heathcheck_broken(monkeypatch):
    def mock_healthcheck(*args, **kwargs):
        mock_response = requests.Response()
        mock_response.status_code = 404

        return mock_response

    monkeypatch.setattr(requests, "get", mock_healthcheck)


def test_check_sirius_available(patched_sirius_heathcheck):
    result = check_sirius_available()

    assert result is True


def test_check_sirius_not_available(patched_sirius_heathcheck_broken):
    result = check_sirius_available()

    assert result is False
