import hypothesis.strategies as st
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
    endpoint="v1/api/public/lpas",
    url_params={
        "lpa-online-tool-id": "A123567890",
    },
)
@settings(max_examples=max_examples, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_build_sirius_url_with_hypothesis(endpoint, url_params, caplog):

    print(f"endpoint: {endpoint}")
    url = test_sirius_service.build_sirius_url(endpoint, url_params)

    assert validators.url(url)
