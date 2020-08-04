import pytest


@pytest.mark.parametrize(
    "sirius_uid, expected_status_code",
    [("700000000013", 200), ("800000000013", 404), ("crash_sirius_with_500", 404)],
)
def test_use_an_lpa_route(
    sirius_uid, expected_status_code, test_server, patched_send_request_to_sirius
):
    response = test_server.get(f"/v1/use-an-lpa/lpas/{sirius_uid}")

    assert response.status_code == expected_status_code
