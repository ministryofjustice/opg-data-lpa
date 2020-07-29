import logging
import urllib

import hypothesis.strategies as st
import pytest
import validators
from hypothesis import given, settings, example

from lambda_functions.v1.functions.lpa.app.api import sirius_service
from lambda_functions.v1.tests.sirius_service.conftest import max_examples


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
@settings(max_examples=max_examples)
def test_build_sirius_url_with_hypothesis(endpoint, url_params, caplog):

    url = sirius_service.build_sirius_url(endpoint, url_params)

    assert validators.url(url)
    with pytest.raises(Exception):
        sirius_service.build_sirius_url(endpoint, url_params)

        with caplog.at_level(logging.ERROR):
            assert "Unable to build Sirius URL" in caplog.text
