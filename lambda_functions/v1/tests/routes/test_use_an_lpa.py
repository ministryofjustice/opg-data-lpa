def test_use_an_lpa_route(test_server):
    fake_sirius_uid = "123456"
    response = test_server.get(f"/v1/use-an-lpa/lpas/{fake_sirius_uid}")

    assert response.status_code == 200
    # assert response.get_json()["message"] == f"OK {fake_sirius_uid}"
