import logging

import hypothesis.strategies as st
import pytest
import validators
from hypothesis import given, settings, example, HealthCheck
from .conftest import (
    max_examples,
    test_sirius_service,
)


@given(
    endpoint=st.text(), url_params=st.dictionaries(st.text(), st.text()),
)
@example(
    endpoint="v1/api/public/documents",
    url_params={
        "metadata[submission_id]": 11111,
        "metadata[report_id]": "d0a43b67-3084-4a74-ab55-a7542cfadd37",
    },
)
@settings(max_examples=max_examples, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_build_sirius_url_with_hypothesis(endpoint, url_params, caplog):

    print(f"endpoint: {endpoint}")
    url = test_sirius_service.build_sirius_url(endpoint, url_params)

    assert validators.url(url)
