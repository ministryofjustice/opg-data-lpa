import json

import hypothesis.strategies as st
from hypothesis import settings, given

from lambda_functions.v1.tests.sirius_service.conftest import (
    max_examples,
    alphabet,
    test_sirius_service,
)


@given(
    test_key_name=st.text(min_size=1, alphabet=alphabet),
    test_key=st.text(min_size=1),
    test_data=st.dictionaries(
        st.text(min_size=1), st.text(min_size=1), min_size=1, max_size=10
    ),
)
@settings(max_examples=max_examples)
def test_get_sirius_data_from_cache(monkeypatch, test_key_name, test_key, test_data):

    test_sirius_service.request_caching_name = test_key_name
    test_cache = test_sirius_service.cache

    full_key = f"{test_key_name}-{test_key}"
    test_cache.set(name=full_key, value=json.dumps(test_data))

    status_code, result_data = test_sirius_service._get_sirius_data_from_cache(
        redis_conn=test_cache, key=test_key
    )

    assert status_code == 200
    assert result_data == test_data

    test_cache.flushall()


def test_get_sirius_data_from_cache_redis_ded(monkeypatch):

    test_key_name = "test_key_name"
    test_key = "test_key"

    test_sirius_service.request_caching_name = test_key_name

    test_cache = test_sirius_service.cache

    status_code, result_data = test_sirius_service._get_sirius_data_from_cache(
        redis_conn=test_cache, key=test_key
    )

    assert status_code == 500
    assert result_data is None

    test_cache.flushall()
