import fakeredis
import pytest

from opg_sirius_service import sirius_handler

from lambda_functions.v1.tests.routes.conftest import mock_redis_server

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
    patched_send_request_to_sirius,
):

    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: sirius_available,
    )

    response = test_server.get(f"/v1/use-an-lpa/lpas/{sirius_uid}")

    mock_redis = fakeredis.FakeStrictRedis(server=mock_redis_server)

    assert response.status_code == expected_status_code
    if cache_expected:
        redis_entry = mock_redis.get(name=f"opg-data-lpa-local-{sirius_uid}-{expected_status_code}")
        print(f"redis_entry: {redis_entry}")
        assert response.get_json() == json.loads(redis_entry)[0]
    else:
        assert mock_redis.exists(f"opg-data-lpa-local-{sirius_uid}-{expected_status_code}") == 0


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
    patched_send_request_to_sirius,
):

    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: sirius_available,
    )

    response = test_server_no_cache.get(f"/v1/use-an-lpa/lpas/{sirius_uid}")

    mock_redis = fakeredis.FakeStrictRedis(server=mock_redis_server)

    assert response.status_code == expected_status_code
    assert mock_redis.exists(f"opg-data-lpa-local-{sirius_uid}-{expected_status_code}") == 0
