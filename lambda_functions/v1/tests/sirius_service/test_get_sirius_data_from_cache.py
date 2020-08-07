import json

import fakeredis
import hypothesis.strategies as st
from hypothesis import settings, given

from lambda_functions.v1.functions.lpa.app.api import sirius_service
from lambda_functions.v1.tests.sirius_service.conftest import max_examples, alphabet


@given(
    test_key_name=st.text(min_size=1, alphabet=alphabet),
    test_key=st.text(min_size=1),
    test_data=st.dictionaries(
        st.text(min_size=1), st.text(min_size=1), min_size=1, max_size=10
    ),
)
@settings(max_examples=max_examples)
def test_get_sirius_data_from_cache(monkeypatch, test_key_name, test_key, test_data):

    monkeypatch.setenv("REQUEST_CACHING_NAME", test_key_name)

    r = fakeredis.FakeStrictRedis(charset="utf-8", decode_responses=True)

    full_key = f"{test_key_name}-{test_key}"
    r.set(name=full_key, value=json.dumps(test_data))

    status_code, result_data = sirius_service.get_sirius_data_from_cache(
        redis_conn=r, key=test_key
    )

    assert status_code == 200
    assert result_data == test_data


def test_get_sirius_data_from_cache_missing_env_var(monkeypatch):
    test_key = "test_key"
    test_data = [{"test": "data"}]
    monkeypatch.delenv("REQUEST_CACHING_NAME")

    r = fakeredis.FakeStrictRedis(charset="utf-8", decode_responses=True)

    full_key = f"default_sirius_cache-{test_key}"
    r.set(name=full_key, value=json.dumps(test_data))

    result = r.get(full_key)
    print(f"result: {type(result)}")
    print(f"json.loads(result): {json.loads(result)}")

    status_code, result_data = sirius_service.get_sirius_data_from_cache(
        redis_conn=r, key=test_key
    )

    assert status_code == 200
    assert result_data == test_data


def test_get_sirius_data_from_cache_redis_ded(monkeypatch):

    test_key_name = "test_key_name"
    test_key = "test_key"

    monkeypatch.setenv("REQUEST_CACHING_NAME", test_key_name)

    r = fakeredis.FakeStrictRedis(charset="utf-8", decode_responses=True)

    status_code, result_data = sirius_service.get_sirius_data_from_cache(
        redis_conn=r, key=test_key
    )

    assert status_code == 500
    assert result_data is None
