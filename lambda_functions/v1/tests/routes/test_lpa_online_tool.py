def test_lpa_online_tool_route(test_server):
    fake_lpa_online_tool_id = "123456"
    response = test_server.get(f"/v1/use-an-lpa/lpas/{fake_lpa_online_tool_id}")

    assert response.status_code == 200
    # assert response.get_json()["message"] == f"OK {fake_lpa_online_tool_id}"
