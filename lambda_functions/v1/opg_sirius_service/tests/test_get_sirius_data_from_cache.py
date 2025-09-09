import json

import fakeredis
import pytest
import hypothesis.strategies as st
from hypothesis import settings, given, HealthCheck

from opg_sirius_service.sirius_handler import SiriusService
from .conftest import (
    max_examples,
    alphabet,
    test_sirius_service,
)
from .default_config import SiriusServiceTestConfig


@given(
    test_key_name=st.text(min_size=1, alphabet=alphabet),
    test_key=st.text(min_size=1),
    test_data=st.dictionaries(
        st.text(min_size=1), st.text(min_size=1), min_size=1, max_size=10
    ),
)
@settings(
    max_examples=max_examples,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
@pytest.mark.parametrize(
    "http_status",
    [
        (200),
        (410),
    ],
)
def test_get_sirius_data_from_cache(
    monkeypatch, test_key_name, test_key, test_data, http_status
):

    test_sirius_service.request_caching_name = test_key_name
    test_cache = test_sirius_service.cache

    full_key = f"{test_key_name}-{test_key}-{http_status}"
    test_cache.set(name=full_key, value=json.dumps(test_data))

    status_code, result_data = test_sirius_service._get_sirius_data_from_cache(
        key=test_key
    )

    assert status_code == http_status
    assert result_data == test_data

    test_cache.flushall()


def test_get_sirius_data_from_cache_key_does_not_exist(monkeypatch):

    test_key_name = "test_key_name"
    test_key = "test_key"

    test_sirius_service.request_caching_name = test_key_name

    test_cache = test_sirius_service.cache

    status_code, result_data = test_sirius_service._get_sirius_data_from_cache(
        key=test_key
    )

    assert status_code == 500
    assert result_data is None

    test_cache.flushall()


def test_get_sirius_data_from_cache_cache_broken(caplog):

    test_key = "test_key"

    fake_redis_server = fakeredis.FakeServer()
    fake_redis_server.connected = False
    test_redis_handler = fakeredis.FakeStrictRedis(
        charset="utf-8", decode_responses=True, server=fake_redis_server
    )
    test_sirius_service = SiriusService(
        config_params=SiriusServiceTestConfig, cache=test_redis_handler
    )

    status_code, result_data = test_sirius_service._get_sirius_data_from_cache(
        key=test_key
    )

    assert status_code == 500
    assert result_data is None

    with caplog.at_level("ERROR"):
        assert "Unable to get from cache" in caplog.text
