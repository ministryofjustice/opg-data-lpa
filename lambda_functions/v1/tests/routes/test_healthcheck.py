import pytest
from lambda_functions.v1.functions.lpa.app.opg_sirius_service import sirius_handler


@pytest.mark.parametrize(
    " sirius_available, cache_available, return_code",
    [(True, True, 200), (True, False, 504), (False, True, 504), (False, False, 504)],
)
def test_healthcheck_route_with_cache(
    test_server, monkeypatch, sirius_available, cache_available, return_code
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: sirius_available,
    )

    monkeypatch.setattr(
        sirius_handler.SiriusService, "check_cache_available", lambda x: cache_available
    )

    response = test_server.get(f"/v1/healthcheck")

    assert response.status_code == return_code
    assert (
        response.get_json()["data"]["sirius-status"] == "OK"
        if sirius_available is True
        else "Unavailable"
    )
    assert (
        response.get_json()["data"]["cache-status"] == "OK"
        if cache_available is True
        else "Unavailable"
    )


@pytest.mark.parametrize(
    "sirius_available, cache_available, return_code",
    [(True, True, 200), (True, False, 200), (False, True, 504), (False, False, 504)],
)
def test_healthcheck_route_no_cache(
    test_server_no_cache, monkeypatch, sirius_available, cache_available, return_code
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: sirius_available,
    )

    monkeypatch.setattr(
        sirius_handler.SiriusService, "check_cache_available", lambda x: cache_available
    )

    response = test_server_no_cache.get(f"/v1/healthcheck")

    assert response.status_code == return_code
    assert (
        response.get_json()["data"]["sirius-status"] == "OK"
        if sirius_available is True
        else "Unavailable"
    )
    assert response.get_json()["data"]["cache-status"] == "Not enabled"
