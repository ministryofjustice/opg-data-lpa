import json

import fakeredis
import pytest

from lambda_functions.v1.functions.lpa.app.sirius_service.sirius_handler import (
    SiriusService,
)
from lambda_functions.v1.config import LocalTestingConfig

test_redis_handler = fakeredis.FakeStrictRedis(charset="utf-8", decode_responses=True)
test_sirius_service = SiriusService(
    config_params=LocalTestingConfig, cache=test_redis_handler
)


sirius_test_data = json.dumps({"sirius": "test_data"})
key = "send_request_to_sirius"
url = "http://not-an-url.com"
full_key = f"{test_sirius_service.request_caching_name}-{key}"
ttl = 48
cache = test_sirius_service.cache


@pytest.fixture()
def mock_sirius_available(monkeypatch):
    monkeypatch.setattr(test_sirius_service, "_check_sirius_available", lambda: True)


@pytest.fixture()
def mock_sirius_not_available(monkeypatch):
    monkeypatch.setattr(test_sirius_service, "_check_sirius_available", lambda: False)


@pytest.fixture()
def mock_get_data_from_sirius_success(monkeypatch):
    monkeypatch.setattr(
        test_sirius_service,
        "_get_data_from_sirius",
        lambda x, y, z, p: (200, sirius_test_data),
    )


@pytest.fixture()
def mock_get_data_from_sirius_failed(monkeypatch):
    monkeypatch.setattr(
        test_sirius_service, "_get_data_from_sirius", lambda x, y, z, p: (500, "error")
    )


@pytest.mark.parametrize(
    "method, cache_enabled, expected_status_code, cache_expected",
    [
        ("GET", "enabled", 200, True),
        ("POST", "enabled", 200, False),
        ("PUT", "enabled", 200, False),
        ("GET", "disabled", 200, False),
        ("POST", "disabled", 200, False),
        ("PUT", "disabled", 200, False),
        ("GET", "banana", 200, False),
        ("GET", None, 200, False),
    ],
)
def test_send_request_to_sirius(
    monkeypatch,
    caplog,
    mock_sirius_available,
    mock_get_data_from_sirius_success,
    method,
    cache_enabled,
    expected_status_code,
    cache_expected,
):
    test_sirius_service.request_caching = cache_enabled

    result_status_code, result_data = test_sirius_service.send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code

    if cache_expected:
        print(f"full_key: {full_key}")
        print(f"cache.get(full_key): {cache.get(full_key)}")
        # print(f"json.loads(cache.get(full_key)): {json.loads(cache.get(full_key))}")
        print(f"cache.scan(): {cache.scan()}")

        assert json.loads(cache.get(full_key)) == sirius_test_data
        assert cache.ttl(full_key) == ttl * 60 * 60

    else:
        assert cache.exists(full_key) == 0

    cache.flushall()


# TODO should this 500 when the GET fails or should it try the cache?
@pytest.mark.parametrize(
    "method, cache_enabled, expected_status_code, cache_expected",
    [
        ("GET", "enabled", 500, False),
        ("POST", "enabled", 500, False),
        ("PUT", "enabled", 500, False),
        ("GET", "disabled", 500, False),
        ("POST", "disabled", 500, False),
        ("PUT", "disabled", 500, False),
    ],
)
def test_send_request_to_sirius_request_fails(
    monkeypatch,
    caplog,
    mock_sirius_available,
    mock_get_data_from_sirius_failed,
    method,
    cache_enabled,
    expected_status_code,
    cache_expected,
):
    test_sirius_service.request_caching = cache_enabled
    result_status_code, result_data = test_sirius_service.send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code
    if cache_expected:

        assert json.loads(cache.get(full_key)) == json.loads(sirius_test_data)
        assert cache.ttl(full_key) == ttl * 60 * 60

    else:
        assert cache.exists(full_key) == 0
    cache.flushall()


@pytest.mark.parametrize(
    "method, cache_enabled, expected_status_code, cache_expected",
    [
        ("GET", "enabled", 200, True),
        ("POST", "enabled", 500, False),
        ("PUT", "enabled", 500, False),
        ("GET", "disabled", 500, False),
        ("POST", "disabled", 500, False),
        ("PUT", "disabled", 500, False),
    ],
)
def test_send_request_to_sirius_but_sirius_is_broken_value_in_cache(
    monkeypatch,
    caplog,
    mock_sirius_not_available,
    mock_get_data_from_sirius_failed,
    method,
    cache_enabled,
    expected_status_code,
    cache_expected,
):

    cache.set(name=f"{full_key}", value=sirius_test_data, ex=ttl * 60 * 60)
    print(f"cache.scan(): {cache.scan()}")

    test_sirius_service.request_caching = cache_enabled

    result_status_code, result_data = test_sirius_service.send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code
    if cache_expected:
        print(f"json.loads(cache.get(full_key)): {json.loads(cache.get(full_key))}")

        assert json.loads(cache.get(full_key)) == json.loads(sirius_test_data)
        assert cache.ttl(full_key) == ttl * 60 * 60

    cache.flushall()


@pytest.mark.parametrize(
    "method, cache_enabled, expected_status_code, cache_expected",
    [
        ("GET", "enabled", 500, False),
        ("POST", "enabled", 500, False),
        ("PUT", "enabled", 500, False),
        ("GET", "disabled", 500, False),
        ("POST", "disabled", 500, False),
        ("PUT", "disabled", 500, False),
    ],
)
def test_send_request_to_sirius_but_sirius_is_broken_value_not_in_cache(
    monkeypatch,
    caplog,
    mock_sirius_not_available,
    mock_get_data_from_sirius_failed,
    method,
    cache_enabled,
    expected_status_code,
    cache_expected,
):
    test_sirius_service.request_caching = cache_enabled

    result_status_code, result_data = test_sirius_service.send_request_to_sirius(
        key, url, method, content_type=None, data=None
    )

    assert result_status_code == expected_status_code
    if cache_expected:

        assert json.loads(cache.get(full_key)) == sirius_test_data
        assert cache.ttl(full_key) == ttl * 60 * 60

    else:
        assert cache.exists(full_key) == 0

    cache.flushall()
