import pytest
import requests

from .conftest import test_sirius_service


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

@pytest.fixture
def patched_sirius_heathcheck_exception(monkeypatch):
    def mock_healthcheck(*args, **kwargs):
        mock_response = requests.exceptions.ConnectionError()

        return mock_response

    monkeypatch.setattr(requests, "get", mock_healthcheck)


def test_check_sirius_available(patched_sirius_heathcheck):
    result = test_sirius_service.check_sirius_available()

    assert result is True


def test_check_sirius_not_available(patched_sirius_heathcheck_broken):
    result = test_sirius_service.check_sirius_available()

    assert result is False

def test_check_sirius_healthcheck_throws(patched_sirius_heathcheck_exception):
    result = test_sirius_service.check_sirius_available()

    assert result is False
