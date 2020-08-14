from lambda_functions.v1.functions.lpa.app.sirius_service import sirius_handler
import pytest


@pytest.mark.parametrize("sirius_available", [(True), (False)])
def test_healthcheck_route_with_cache(test_server, monkeypatch, sirius_available):

    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: sirius_available,
    )

    response = test_server.get(f"/v1/healthcheck")

    assert response.status_code == 200
    assert response.get_json() == "OK"


@pytest.mark.parametrize("sirius_available", [(True), (False)])
def test_healthcheck_route_no_cache(
    test_server_no_cache, monkeypatch, sirius_available
):

    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: sirius_available,
    )

    response = test_server_no_cache.get(f"/v1/healthcheck")

    assert response.status_code == 200
    assert response.get_json() == "OK"
