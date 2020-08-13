import fakeredis
import pytest

from lambda_functions.v1.functions.lpa.app.sirius_service import sirius_handler

from lambda_functions.v1.tests.routes.conftest import mock_redis_server

import json


@pytest.mark.parametrize(
    "online_tool_id, sirius_available, expected_status_code, cache_expected",
    [
        ("A39721583862", True, 200, True),  # pragma: allowlist secret
        ("A39721583862", False, 200, True),  # pragma: allowlist secret
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
    patched_send_request_to_sirius,
):

    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "_check_sirius_available",
        lambda x: sirius_available,
    )

    response = test_server.get(f"/v1/lpa-online-tool/lpas/{online_tool_id}")

    mock_redis = fakeredis.FakeStrictRedis(server=mock_redis_server)

    assert response.status_code == expected_status_code
    if cache_expected:
        redis_entry = mock_redis.get(name=f"opg-data-lpa-local-{online_tool_id}")
        assert response.get_json() == json.loads(redis_entry)[0]
    else:
        assert mock_redis.exists(f"opg-data-lpa-local-{online_tool_id}") == 0


@pytest.mark.parametrize(
    "online_tool_id, sirius_available, expected_status_code",
    [
        ("A39721583864", True, 200),  # pragma: allowlist secret
        ("A39721583864", False, 404),  # pragma: allowlist secret
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
    patched_send_request_to_sirius,
):

    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "_check_sirius_available",
        lambda x: sirius_available,
    )

    response = test_server_no_cache.get(f"/v1/lpa-online-tool/lpas/{online_tool_id}")

    mock_redis = fakeredis.FakeStrictRedis(server=mock_redis_server)

    assert response.status_code == expected_status_code
    assert mock_redis.exists(f"opg-data-lpa-local-{online_tool_id}") == 0
