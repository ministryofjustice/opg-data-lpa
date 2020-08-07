import logging

import pytest

from lambda_functions.v1.functions.lpa.app.api import sirius_service
from lambda_functions.v1.functions.lpa.app.api.sirius_service import (
    send_request_to_sirius,
)


@pytest.fixture()
def mock_caching_enabled(monkeypatch):
    monkeypatch.setenv("REQUEST_CACHING", "enabled")


@pytest.fixture()
def mock_caching_disabled(monkeypatch):
    monkeypatch.setenv("REQUEST_CACHING", "disabled")


@pytest.fixture()
def mock_sirius_available(monkeypatch):
    monkeypatch.setattr(sirius_service, "check_sirius_available", lambda: True)


@pytest.fixture()
def mock_sirius_not_available(monkeypatch):
    monkeypatch.setattr(sirius_service, "check_sirius_available", lambda: False)


@pytest.fixture()
def mock_get_data_from_sirius_success(monkeypatch):
    monkeypatch.setattr(
        sirius_service, "get_data_from_sirius", lambda x, y, z, p: (200, "OK")
    )


@pytest.fixture()
def mock_get_data_from_sirius_failed(monkeypatch):
    monkeypatch.setattr(
        sirius_service, "get_data_from_sirius", lambda x, y, z, p: (500, "error")
    )


@pytest.fixture()
def mock_put_data_in_cache_success(monkeypatch):
    monkeypatch.setattr(
        sirius_service, "put_sirius_data_in_cache", lambda redis_conn, key, data: True
    )


@pytest.fixture()
def mock_put_data_in_cache_failed(monkeypatch):
    monkeypatch.setattr(
        sirius_service, "put_sirius_data_in_cache", lambda redis_conn, key, data: False
    )


@pytest.fixture()
def mock_get_data_from_cache_success(monkeypatch):
    monkeypatch.setattr(
        sirius_service,
        "get_sirius_data_from_cache",
        lambda redis_conn, key: (200, {"test": "data"}),
    )


@pytest.fixture()
def mock_get_data_from_cache_failed(monkeypatch):
    monkeypatch.setattr(
        sirius_service,
        "get_sirius_data_from_cache",
        lambda redis_conn, key: (500, None),
    )


@pytest.mark.parametrize(
    "method, expected_status_code", [("GET", 200), ("POST", 200), ("PUT", 200)]
)
def test_send_request_to_sirius(
    monkeypatch,
    caplog,
    mock_caching_enabled,
    mock_sirius_available,
    mock_get_data_from_sirius_success,
    mock_put_data_in_cache_success,
    method,
    expected_status_code,
):

    key = "test_key"
    url = "http://not-an-url.com"

    result_status_code, result_data = send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code

    with caplog.at_level(logging.INFO):
        if method == "GET":
            assert "Putting data in cache with key" in caplog.text
        else:
            assert "Putting data in cache with key" not in caplog.text


@pytest.mark.parametrize(
    "method, expected_status_code", [("GET", 200), ("POST", 200), ("PUT", 200)]
)
def test_send_request_to_sirius_no_cache(
    monkeypatch,
    caplog,
    mock_caching_disabled,
    mock_sirius_available,
    mock_get_data_from_sirius_success,
    mock_put_data_in_cache_success,
    method,
    expected_status_code,
):

    key = "test_key"
    url = "http://not-an-url.com"

    result_status_code, result_data = send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code

    with caplog.at_level(logging.INFO):
        assert "Putting data in cache with key" not in caplog.text


@pytest.mark.parametrize(
    "method, expected_status_code", [("GET", 200), ("POST", 200), ("PUT", 200)]
)
def test_send_request_to_sirius_no_cache_env_var(
    monkeypatch,
    caplog,
    mock_sirius_available,
    mock_get_data_from_sirius_success,
    mock_put_data_in_cache_success,
    method,
    expected_status_code,
):

    monkeypatch.delenv("REQUEST_CACHING")

    key = "test_key"
    url = "http://not-an-url.com"

    result_status_code, result_data = send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code

    with caplog.at_level(logging.INFO):
        assert "Putting data in cache with key" not in caplog.text


# TODO should this 500 when the GET fails or should it try the cache?
@pytest.mark.parametrize(
    "method, expected_status_code", [("GET", 500), ("POST", 500), ("PUT", 500)]
)
def test_send_request_to_sirius_request_fails(
    monkeypatch,
    caplog,
    mock_caching_enabled,
    mock_sirius_available,
    mock_get_data_from_sirius_failed,
    mock_put_data_in_cache_success,
    method,
    expected_status_code,
):

    key = "test_key"
    url = "http://not-an-url.com"

    result_status_code, result_data = send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code

    with caplog.at_level(logging.INFO):
        "Putting data in cache with key" not in caplog.text


@pytest.mark.parametrize(
    "method, expected_status_code", [("GET", 500), ("POST", 500), ("PUT", 500)]
)
def test_send_request_to_sirius_no_cache_request_fails(
    monkeypatch,
    caplog,
    mock_caching_disabled,
    mock_sirius_available,
    mock_get_data_from_sirius_failed,
    mock_put_data_in_cache_success,
    method,
    expected_status_code,
):

    key = "test_key"
    url = "http://not-an-url.com"

    result_status_code, result_data = send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code

    with caplog.at_level(logging.INFO):
        assert "Putting data in cache with key" not in caplog.text


@pytest.mark.parametrize(
    "method, expected_status_code", [("GET", 200), ("POST", 500), ("PUT", 500)]
)
def test_send_request_to_sirius_but_sirius_is_broken(
    monkeypatch,
    caplog,
    mock_caching_enabled,
    mock_sirius_not_available,
    mock_get_data_from_sirius_failed,
    mock_get_data_from_cache_success,
    method,
    expected_status_code,
):

    key = "test_key"
    url = "http://not-an-url.com"

    result_status_code, result_data = send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code

    with caplog.at_level(logging.INFO):
        if method == "GET":
            assert "Getting data from cache with key" in caplog.text
        else:
            assert "Getting data from cache with key" not in caplog.text


@pytest.mark.parametrize(
    "method, expected_status_code", [("GET", 500), ("POST", 500), ("PUT", 500)]
)
def test_send_request_to_sirius_but_sirius_is_broken_value_not_in_cache(
    monkeypatch,
    caplog,
    mock_caching_enabled,
    mock_sirius_not_available,
    mock_get_data_from_sirius_failed,
    mock_get_data_from_cache_failed,
    method,
    expected_status_code,
):

    key = "test_key"
    url = "http://not-an-url.com"

    result_status_code, result_data = send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code

    with caplog.at_level(logging.INFO):
        if method == "GET":
            assert "Getting data from cache with key" in caplog.text
        else:
            assert "Getting data from cache with key" not in caplog.text


@pytest.mark.parametrize(
    "method, expected_status_code", [("GET", 500), ("POST", 500), ("PUT", 500)]
)
def test_send_request_to_sirius_but_sirius_is_broken_and_cache_disabled(
    monkeypatch,
    caplog,
    mock_caching_disabled,
    mock_sirius_not_available,
    mock_get_data_from_sirius_failed,
    mock_get_data_from_cache_success,
    method,
    expected_status_code,
):

    key = "test_key"
    url = "http://not-an-url.com"

    result_status_code, result_data = send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code

    with caplog.at_level(logging.INFO):
        assert "Getting data from cache with key" not in caplog.text
