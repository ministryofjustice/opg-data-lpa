def test_healthcheck_route(test_server):

    response = test_server.get(f"/v1/healthcheck")

    assert response.status_code == 200
    assert response.get_json() == "OK"
