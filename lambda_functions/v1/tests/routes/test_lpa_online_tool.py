import pytest


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
