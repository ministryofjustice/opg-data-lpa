import logging

import pytest

from lambda_functions.v1.functions.lpa.app.api import sirius_service
from lambda_functions.v1.functions.lpa.app.api.sirius_service import (
    send_request_to_sirius,
)


@pytest.mark.parametrize(
    "method, expected_status_code", [("GET", 200), ("POST", 200), ("PUT", 200)]
)
def test_send_request_to_sirius(monkeypatch, caplog, method, expected_status_code):
    """
    Sirius is available, cache enabled, request works and puts data in cache
    """

    monkeypatch.setenv("REQUEST_CACHING", "enabled")
    monkeypatch.setattr(sirius_service, "check_sirius_available", lambda: True)
    monkeypatch.setattr(
        sirius_service, "get_data_from_sirius", lambda x, y, z, p: (200, "OK")
    )
    monkeypatch.setattr(sirius_service, "put_sirius_data_in_cache", lambda x, y: True)

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
    monkeypatch, caplog, method, expected_status_code
):
    """
    Sirius is available, cache disabled, request works
    """

    monkeypatch.setenv("REQUEST_CACHING", "disabled")
    monkeypatch.setattr(sirius_service, "check_sirius_available", lambda: True)
    monkeypatch.setattr(
        sirius_service, "get_data_from_sirius", lambda x, y, z, p: (200, "OK")
    )
    monkeypatch.setattr(sirius_service, "put_sirius_data_in_cache", lambda x, y: True)

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
    monkeypatch, caplog, method, expected_status_code
):
    """
    Sirius is available, cache disabled, request works
    """

    monkeypatch.delenv("REQUEST_CACHING")
    monkeypatch.setattr(sirius_service, "check_sirius_available", lambda: True)
    monkeypatch.setattr(
        sirius_service, "get_data_from_sirius", lambda x, y, z, p: (200, "OK")
    )
    monkeypatch.setattr(sirius_service, "put_sirius_data_in_cache", lambda x, y: True)

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
    monkeypatch, caplog, method, expected_status_code
):
    """
    Sirius is available, cache enabled,  request fails
    """

    monkeypatch.setenv("REQUEST_CACHING", "enabled")
    monkeypatch.setattr(sirius_service, "check_sirius_available", lambda: True)
    monkeypatch.setattr(
        sirius_service, "get_data_from_sirius", lambda x, y, z, p: (500, "error")
    )
    monkeypatch.setattr(sirius_service, "put_sirius_data_in_cache", lambda x, y: True)

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
    monkeypatch, caplog, method, expected_status_code
):
    """
    Sirius is available, cache disabled, request fails
    """

    monkeypatch.setenv("REQUEST_CACHING", "disabled")
    monkeypatch.setattr(sirius_service, "check_sirius_available", lambda: True)
    monkeypatch.setattr(
        sirius_service, "get_data_from_sirius", lambda x, y, z, p: (500, "error")
    )
    monkeypatch.setattr(sirius_service, "put_sirius_data_in_cache", lambda x, y: True)

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
    monkeypatch, caplog, method, expected_status_code
):
    """
    Sirius is not available, cache enabled, request fails, cache works
    """

    monkeypatch.setenv("REQUEST_CACHING", "enabled")
    monkeypatch.setattr(sirius_service, "check_sirius_available", lambda: False)
    monkeypatch.setattr(
        sirius_service, "get_data_from_sirius", lambda x, y, z, p: (500, "errpr")
    )
    monkeypatch.setattr(
        sirius_service, "get_sirius_data_from_cache", lambda x: (200, {"test": "data"})
    )

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
    monkeypatch, caplog, method, expected_status_code
):
    """
    Sirius is not available, cache enabled, request fails and value not in cache
    """

    monkeypatch.setenv("REQUEST_CACHING", "enabled")
    monkeypatch.setattr(sirius_service, "check_sirius_available", lambda: False)
    monkeypatch.setattr(
        sirius_service, "get_data_from_sirius", lambda x, y, z, p: (500, "errpr")
    )
    monkeypatch.setattr(
        sirius_service, "get_sirius_data_from_cache", lambda x: (500, None)
    )

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
    monkeypatch, caplog, method, expected_status_code
):
    """
    Sirius is not available, cache disabled, request works, cache works
    """

    monkeypatch.setenv("REQUEST_CACHING", "disabled")
    monkeypatch.setattr(sirius_service, "check_sirius_available", lambda: False)
    monkeypatch.setattr(
        sirius_service, "get_data_from_sirius", lambda x, y, z, p: (500, "error")
    )
    monkeypatch.setattr(
        sirius_service, "get_sirius_data_from_cache", lambda x: (200, {"test": "data"})
    )

    key = "test_key"
    url = "http://not-an-url.com"

    result_status_code, result_data = send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code

    with caplog.at_level(logging.INFO):
        assert "Getting data from cache with key" not in caplog.text
