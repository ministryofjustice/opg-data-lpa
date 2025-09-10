import pytest

from lambda_functions.v1.functions.lpa.opg_sirius_service import sirius_handler
from pact.v3 import match

import json


@pytest.mark.parametrize(
    "sirius_uid, sirius_available, expected_status_code, cache_expected",
    [
        ("700000000013", True, 200, True),
        ("700000000013", False, 200, True),
        ("800000000014", True, 404, False),
        ("800000000014", False, 404, False),
        ("crash_sirius_with_500", True, 404, False),
        ("crash_sirius_with_500", False, 404, False),
    ],
)
def test_use_an_lpa_route_with_cache(
    monkeypatch,
    sirius_uid,
    sirius_available,
    expected_status_code,
    cache_expected,
    test_server,
    cache,
    mock_environ,
    patched_send_request_to_sirius,
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: sirius_available,
    )

    response = test_server.get(
        f"/v1/use-an-lpa/lpas/{sirius_uid}", environ_base=mock_environ
    )

    assert response.status_code == expected_status_code
    if cache_expected:
        redis_entry = cache.get(
            name=f"opg-data-lpa-local-{sirius_uid}-{expected_status_code}"
        )
        print(f"redis_entry: {redis_entry}")
        assert response.get_json() == json.loads(redis_entry)[0]
    else:
        assert (
            cache.exists(f"opg-data-lpa-local-{sirius_uid}-{expected_status_code}") == 0
        )


@pytest.mark.parametrize(
    "sirius_uid, sirius_available, expected_status_code",
    [
        ("700000000015", True, 200),
        ("700000000015", False, 404),
        ("800000000016", True, 404),
        ("800000000016", False, 404),
        ("crash_sirius_with_500", True, 404),
        ("crash_sirius_with_500", False, 404),
    ],
)
def test_use_an_lpa_route_no_cache(
    monkeypatch,
    sirius_uid,
    sirius_available,
    expected_status_code,
    test_server_no_cache,
    cache,
    mock_environ,
    patched_send_request_to_sirius,
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: sirius_available,
    )

    response = test_server_no_cache.get(
        f"/v1/use-an-lpa/lpas/{sirius_uid}", environ_base=mock_environ
    )

    assert response.status_code == expected_status_code
    assert cache.exists(f"opg-data-lpa-local-{sirius_uid}-{expected_status_code}") == 0


def test_use_an_lpa_pact(
    monkeypatch,
    app,
    pact,
    cache,
    mock_environ,
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: True,
    )

    expected = match.each_like(
        {
            "uId": match.regex("7000-3764-4871", regex=r"^7\d{3}-\d{4}-\d{4}$"),
            "status": match.like("Pending"),
        },
        min=1,
    )

    (
        pact.upon_receiving("A request for LPA 7000-3764-4871")
        .given("An LPA with UID 7000-3764-4871 exists")
        .with_request("get", "/api/public/v1/lpas")
        .with_query_parameter("uid", "700037644871")
        .will_respond_with(200)
        .with_body(expected)
    )

    with pact.serve() as srv:
        app.sirius.sirius_base_url = srv.url

        response = app.test_client().get(
            f"/v1/use-an-lpa/lpas/700037644871", environ_base=mock_environ
        )

        assert response.status_code == 200
        redis_entry = cache.get(name=f"opg-data-lpa-local-700037644871-200")
        assert response.get_json() == json.loads(redis_entry)[0]
