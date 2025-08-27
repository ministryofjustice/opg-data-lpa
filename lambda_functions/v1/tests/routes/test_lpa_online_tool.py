import pytest

from opg_sirius_service import sirius_handler
from pact import EachLike, Like, Term

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
    test_server_pact,
    pact,
    cache,
    mock_environ,
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: True,
    )

    expected = EachLike(
        {
            "status": Like("Registered"),
            "cancellationDate": Term(r"^\d{1,2}/\d{1,2}/\d{4}$", "28/08/2020"),
            "dispatchDate": "28/08/2020",
            "invalidDate": "28/08/2020",
            "onlineLpaId": "28/08/2020",
            "receiptDate": "28/08/2020",
            "registrationDate": "28/08/2020",
            "rejectedDate": "28/08/2020",
            "statusDate": "28/08/2020",
            "withdrawnDate": "28/08/2020",
        },
        minimum=1,
    )

    (
        pact.given("An LPA with Online LPA ID A17843895384 exists")
        .upon_receiving(f"A request for LPA A17843895384")
        .with_request(
            method="get",
            path=f"/api/public/v1/lpas",
            query={"lpa-online-tool-id": "A17843895384"},
        )
        .will_respond_with(200, body=expected)
    )

    with pact:
        response = test_server_pact.get(
            f"/v1/lpa-online-tool/lpas/A17843895384", environ_base=mock_environ
        )

        assert response.status_code == 200
        redis_entry = cache.get(name=f"opg-data-lpa-local-A17843895384-200")
        assert response.get_json() == json.loads(redis_entry)[0]
