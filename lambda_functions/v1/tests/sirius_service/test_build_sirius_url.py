import urllib

import pytest

from lambda_functions.v1.functions.lpa.app.api import sirius_service


@pytest.mark.parametrize(
    "base_url, version, endpoint, url_params, expected_result",
    [
        (
            "https://frontend-feature5.dev.sirius.opg.digital/api/public",
            "v1",
            "documents",
            None,
            "https://frontend-feature5.dev.sirius.opg.digital/api/public"
            "/v1/documents",
        ),
        (
            "https://frontend-feature5.dev.sirius.opg.digital/api/public",
            None,
            "health-check/service-status",
            None,
            "https://frontend-feature5.dev.sirius.opg.digital/api/public/"
            "health-check/service-status",
        ),
        (
            "https://frontend-feature5.dev.sirius.opg.digital/api/public",
            "v1",
            "clients/12345678/reports/7230e5a2-312b-4b50-bc09-f9c00c6b7f1d",
            None,
            "https://frontend-feature5.dev.sirius.opg.digital/api/public/v1/clients/123"
            "45678/reports/7230e5a2-312b-4b50-bc09-f9c00c6b7f1d",
        ),
        (
            "https://frontend-feature5.dev.sirius.opg.digital/api/public",
            "v1",
            "clients/12345678/documents",
            {
                "metadata[submission_id]": 11111,
                "metadata[report_id]": "d0a43b67-3084-4a74-ab55-a7542cfadd37",
            },
            "https://frontend-feature5.dev.sirius.opg.digital/api/public/v1/clients/123"
            "45678/documents?metadata[submission_id]=11111&metadata[report_id]=d0a43b67"
            "-3084-4a74-ab55-a7542cfadd37",
        ),
        (
            "http://www.fake_url.com",
            "6.3.1",
            "random/endpoint/",
            None,
            "http://www.fake_url.com/6.3.1/random/endpoint/",
        ),
    ],
)
def test_build_sirius_url(base_url, version, endpoint, url_params, expected_result):
    # Copied directly from original
    # "lambda_functions/v1/tests/reports/test_reports_sirius_service.py' test
    url = sirius_service.build_sirius_url(base_url, version, endpoint, url_params)

    assert urllib.parse.unquote(url) == expected_result


def test_build_sirius_url_error():
    base_url = "banana"
    version = "30"
    endpoint = "random/endpoint/"
    url_params = None
    with pytest.raises(Exception):
        url = sirius_service.build_sirius_url(base_url, version, endpoint, url_params)

        print(f"url: {url}")

        assert 1 == 3
