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
    test_ttl=st.integers(min_value=1, max_value=100),
)
@settings(max_examples=max_examples)
def test_put_sirius_data_in_cache(
    monkeypatch, test_key_name, test_key, test_data, test_ttl
):

    monkeypatch.setenv("REQUEST_CACHING_NAME", test_key_name)
    monkeypatch.setenv("REQUEST_CACHING_TTL", str(test_ttl))

    r = fakeredis.FakeStrictRedis(charset="utf-8", decode_responses=True)

    sirius_service.put_sirius_data_in_cache(
        redis_conn=r, key=test_key, data=json.dumps(test_data)
    )

    full_key = f"{test_key_name}-{test_key}"

    assert json.loads(json.loads(r.get(full_key))) == test_data
    assert r.ttl(full_key) == test_ttl * 60 * 60

    r.flushall()


def test_put_sirius_data_in_cache_missing_env_vars(monkeypatch):

    monkeypatch.delenv("REQUEST_CACHING_NAME")
    monkeypatch.delenv("REQUEST_CACHING_TTL")

    test_key = "test_key"
    test_data = {"test": "data"}

    r = fakeredis.FakeStrictRedis(charset="utf-8", decode_responses=True)

    sirius_service.put_sirius_data_in_cache(
        redis_conn=r, key=test_key, data=json.dumps(test_data)
    )

    full_key = f"default_sirius_cache-{test_key}"

    assert json.loads(json.loads(r.get(full_key))) == test_data
    assert r.ttl(full_key) == 48 * 60 * 60

    r.flushall()
