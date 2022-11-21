import base64

import pytest
from opg_sirius_service import sirius_handler


def test_request_code_route(
    monkeypatch,
    test_server_no_cache,
    patched_send_request_to_sirius,
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: True,
    )

    response = test_server_no_cache.post(
        "/v1/use-an-lpa/lpas/requestCode",
        method='POST',
        content_type="application/json",
        data='{"case_uid":70001,"actor_uid":70005}'
    )

    assert response.status_code == 204


def test_dict_body_works_as_json(
    monkeypatch,
    test_server_no_cache,
    patched_send_request_to_sirius,
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: True,
    )

    response = test_server_no_cache.post(
        "/v1/use-an-lpa/lpas/requestCode",
        method='POST',
        content_type="application/json",
        data='{"case_uid": 70001, "actor_uid": 70005}'
    )

    assert response.status_code == 204


def test_request_code_route_sirius_unavailable(
    monkeypatch,
    test_server_no_cache,
    patched_send_request_to_sirius,
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: False,
    )

    response = test_server_no_cache.post(
        "/v1/use-an-lpa/lpas/requestCode",
        method='POST',
        content_type="application/json",
        data='{"case_uid":70001,"actor_uid":70005}'
    )

    assert response.status_code == 500
