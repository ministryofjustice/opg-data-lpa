import json

import hypothesis.strategies as st
from hypothesis import given, settings, example, HealthCheck

from .conftest import max_examples
from .strategies import (
    url_as_string,
    content_type,
)

from .conftest import test_sirius_service


@given(
    url=url_as_string(),
    method=st.sampled_from(["GET", "POST", "PUT"]),
    content_type=content_type(),
    data=st.dictionaries(st.text(), st.text()),
)
@example(url="http://not-an-url.com", method="GET", content_type=None, data=None)
@example(url="http://not-an-url.com", method="POST", content_type=None, data=None)
@example(url="http://not-an-url.com", method="PUT", content_type=None, data=None)
@settings(max_examples=max_examples, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_get_data_from_sirius(
    url, method, content_type, data, patched_build_sirius_headers, patched_requests
):
    default_content_type = "application/json"

    result_status, result_data = test_sirius_service._get_data_from_sirius(
        url=url, method=method, content_type=content_type, data=json.dumps(data)
    )

    assert result_status == 200
    assert result_data["request_type"].lower() == method.lower()
    if content_type:
        assert result_data["headers"]["Content-Type"] == content_type
    else:
        assert result_data["headers"]["Content-Type"] == default_content_type
    if method in ["POST", "PUT"]:
        assert len(result_data["data"]) > 0
    if method in ["GET"]:
        assert result_data["data"] is None


def test_get_data_from_sirius_bad_method(
    patched_build_sirius_headers, patched_requests
):
    url = "http://not-an-url.com"
    method = "banana"

    result_status, result_data = test_sirius_service._get_data_from_sirius(
        url=url, method=method
    )

    assert result_status == 500
    assert (
        result_data == f"Unable to send request to Sirius, details: Method "
        f"{method} "
        f"not allowed on Sirius route"
    )


def test_get_data_from_sirius_exception(
    patched_build_sirius_headers, patched_requests_broken, caplog
):
    url = "http://not-an-url.com"
    method = "GET"

    result_status, result_data = test_sirius_service._get_data_from_sirius(
        url=url, method=method
    )
    assert result_status == 500
