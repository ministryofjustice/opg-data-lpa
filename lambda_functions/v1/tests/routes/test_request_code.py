from opg_sirius_service import sirius_handler


def test_request_code_route(
    monkeypatch,
    test_server_no_cache,
    patched_send_request_to_sirius,
    mock_environ,
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: True,
    )

    response = test_server_no_cache.post(
        "/v1/use-an-lpa/lpas/requestCode",
        method="POST",
        content_type="application/json",
        data='{"case_uid":70001,"actor_uid":70005}',
        environ_base=mock_environ,
    )

    assert response.status_code == 204


def test_dict_body_works_as_json(
    monkeypatch,
    test_server_no_cache,
    patched_send_request_to_sirius,
    mock_environ,
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: True,
    )

    response = test_server_no_cache.post(
        "/v1/use-an-lpa/lpas/requestCode",
        method="POST",
        content_type="application/json",
        data='{"case_uid": 70001, "actor_uid": 70005}',
        environ_base=mock_environ,
    )

    assert response.status_code == 204


def test_request_code_route_sirius_unavailable(
    monkeypatch,
    test_server_no_cache,
    patched_send_request_to_sirius,
    mock_environ,
):
    monkeypatch.setattr(
        sirius_handler.SiriusService,
        "check_sirius_available",
        lambda x: False,
    )

    response = test_server_no_cache.post(
        "/v1/use-an-lpa/lpas/requestCode",
        method="POST",
        content_type="application/json",
        data='{"case_uid":70001,"actor_uid":70005}',
        environ_base=mock_environ,
    )

    assert response.status_code == 500


# def test_request_code_pact(
#     monkeypatch,
#     test_server_pact,
#     pact,
#     mock_environ,
# ):
#     monkeypatch.setattr(
#         sirius_handler.SiriusService,
#         "check_sirius_available",
#         lambda x: True,
#     )

#     (
#         pact.given("An LPA with UID 7000-3764-4871 exists")
#         .upon_receiving(f"A request for a new code on LPA 7000-3764-4871")
#         .with_request(
#             method="post",
#             path=f"/api/public/v1/lpas/requestCode",
#             body={
#                 "case_uid": 700037644871,
#                 "actor_uid": 700028382199,
#             },
#         )
#         .will_respond_with(204)
#     )

#     with pact:
#         response = test_server_pact.post(
#             "/v1/use-an-lpa/lpas/requestCode",
#             method="POST",
#             content_type="application/json",
#             data='{"case_uid":700037644871,"actor_uid":700028382199}',
#             environ_base=mock_environ,
#         )

#         print(response.text)

#         assert response.status_code == 204
