import json

import fakeredis
import hypothesis.strategies as st
from hypothesis import settings, given


from lambda_functions.v1.tests.sirius_service.conftest import (
    max_examples,
    alphabet,
    test_sirius_service,
)


test_cache = test_sirius_service.cache


@given(
    test_key_name=st.text(min_size=1, alphabet=alphabet),
    test_key=st.text(min_size=1),
    test_data=st.dictionaries(
        st.text(min_size=1), st.text(min_size=1), min_size=1, max_size=10
    ),
    test_ttl=st.integers(min_value=1, max_value=100),
)
@settings(max_examples=max_examples)
def test_put_sirius_data_in_cache(test_key_name, test_key, test_data, test_ttl):

    test_sirius_service.request_caching_name = test_key_name
    test_sirius_service.request_caching_ttl = test_ttl

    test_sirius_service._put_sirius_data_in_cache(
        redis_conn=test_cache, key=test_key, data=json.dumps(test_data)
    )

    full_key = f"{test_key_name}-{test_key}"

    assert json.loads(json.loads(test_cache.get(full_key))) == test_data
    assert test_cache.ttl(full_key) == test_ttl * 60 * 60

    test_cache.flushall()