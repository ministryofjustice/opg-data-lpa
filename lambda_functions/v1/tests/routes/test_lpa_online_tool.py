import fakeredis
import pytest
import redis

from lambda_functions.v1.functions.lpa import app
from lambda_functions.v1.tests.routes.conftest import mock_redis_server

import json


@pytest.mark.parametrize(
    "online_tool_id, expected_status_code",
    [
        ("A39721583862", 200),  # pragma: allowlist secret
        ("B39721583862", 404),  # pragma: allowlist secret
        ("crash_sirius_with_500", 404),  # pragma: allowlist secret
    ],
)
def test_lpa_online_tool_route(
    online_tool_id, expected_status_code, test_server, patched_send_request_to_sirius
):
    response = test_server.get(f"/v1/lpa-online-tool/lpas/{online_tool_id}")

    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "online_tool_id, expected_status_code, cache_expected",
    [
        ("A39721583862", 200, True),  # pragma: allowlist secret
        ("B39721583862", 404, False),  # pragma: allowlist secret
        ("crash_sirius_with_500", 404, False),  # pragma: allowlist secret
    ],
)
def test_lpa_online_tool_route_with_cache(
    monkeypatch,
    online_tool_id,
    expected_status_code,
    cache_expected,
    test_server,
    patched_send_request_to_sirius,
    patched_send_request_to_sirius_available,
):

    first_request = test_server.get(f"/v1/lpa-online-tool/lpas/{online_tool_id}")

    mock_redis = fakeredis.FakeStrictRedis(server=mock_redis_server)

    assert first_request.status_code == expected_status_code
    if cache_expected:
        redis_entry = mock_redis.get(name=f"opg-data-lpa-local-{online_tool_id}")
        assert first_request.get_json() == json.loads(redis_entry)[0]
    else:
        assert mock_redis.exists(f"opg-data-lpa-local-{online_tool_id}") == 0
