import pytest

from opg_sirius_service import sirius_handler
from pact.v3 import match

import json


@pytest.mark.parametrize(
    "online_tool_id, sirius_available, expected_status_code, cache_expected",
    [
        ("A39721583862", True, 200, True),  # pragma: allowlist secret
        ("A39721583862", False, 200, True),  # pragma: allowlist secret
        ("A39721583867", True, 410, True),  # pragma: allowlist secret
        ("A39721583867", False, 410, True),  # pragma: allowlist secret
        ("B39721583863", True, 404, False),  # pragma: allowlist secret
        ("B39721583863", False, 404, False),  # pragma: allowlist secret
        ("crash_sirius_with_500", True, 404, False),  # pragma: allowlist secret
        ("crash_sirius_with_500", False, 404, False),  # pragma: allowlist secret
    ],
)
def test_lpa_online_tool_route_with_cache(
    monkeypatch,
    online_tool_id,
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
    # with test_server.app.test_request_context(environ=environ):
    response = test_server.get(
        f"/v1/lpa-online-tool/lpas/{online_tool_id}", environ_base=mock_environ
    )
    assert response.status_code == expected_status_code
    if cache_expected:
        redis_entry = cache.get(
            name=f"opg-data-lpa-local-{online_tool_id}-{expected_status_code}"
        )
        print(f"redis: {redis_entry}")
        if expected_status_code == 410:
            assert response.get_json() == ""
        else:
            assert response.get_json() == json.loads(redis_entry)[0]
    else:
        assert (
            cache.exists(f"opg-data-lpa-local-{online_tool_id}-{expected_status_code}")
            == 0
        )


@pytest.mark.parametrize(
    "online_tool_id, sirius_available, expected_status_code",
    [
        ("A39721583864", True, 200),  # pragma: allowlist secret
        ("A39721583864", False, 404),  # pragma: allowlist secret
        ("A39721583868", True, 410),  # pragma: allowlist secret
        ("A39721583868", False, 404),  # pragma: allowlist secret
        ("B39721583865", True, 404),  # pragma: allowlist secret
        ("B39721583865", False, 404),  # pragma: allowlist secret
        ("crash_sirius_with_500", True, 404),  # pragma: allowlist secret
        ("crash_sirius_with_500", False, 404),  # pragma: allowlist secret
    ],
)
def test_lpa_online_tool_route_no_cache(
    monkeypatch,
    online_tool_id,
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
        f"/v1/lpa-online-tool/lpas/{online_tool_id}", environ_base=mock_environ
    )

    assert response.status_code == expected_status_code
    assert (
        cache.exists(f"opg-data-lpa-local-{online_tool_id}-{expected_status_code}") == 0
    )


def test_lpa_online_tool_pact(
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
            "status": match.like("Cancelled"),
            "onlineLpaId": match.regex("A17843895384", regex=r"^A\d{11}$"),
            "receiptDate": match.regex("28/08/2020", regex=r"^\d{1,2}/\d{1,2}/\d{4}$"),
            "statusDate": match.regex("28/08/2020", regex=r"^\d{1,2}/\d{1,2}/\d{4}$"),
            "cancellationDate": match.regex(
                "28/08/2020", regex=r"^\d{1,2}/\d{1,2}/\d{4}$"
            ),
            "dispatchDate": match.none(),
            "invalidDate": match.none(),
            "registrationDate": match.none(),
            "rejectedDate": match.none(),
            "withdrawnDate": match.none(),
        },
        min=1,
    )

    (
        pact.upon_receiving("A request for LPA A17843895384")
        .given("A cancelled LPA with Online LPA ID A17843895384 exists")
        .with_request("get", "/api/public/v1/lpas")
        .with_query_parameter("lpa-online-tool-id", "A17843895384")
        .will_respond_with(200)
        .with_body(expected)
    )

    with pact.serve() as srv:
        app.sirius.sirius_base_url = srv.url

        response = app.test_client().get(
            f"/v1/lpa-online-tool/lpas/A17843895384", environ_base=mock_environ
        )

        assert response.status_code == 200
        redis_entry = cache.get(name=f"opg-data-lpa-local-A17843895384-200")
        assert response.get_json() == json.loads(redis_entry)[0]
