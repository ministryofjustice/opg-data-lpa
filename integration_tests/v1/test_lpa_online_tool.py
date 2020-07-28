import pytest
import json
from .conftest import send_a_request, configs_to_test, is_valid_schema


@pytest.mark.parametrize("test_config", configs_to_test)
def test_online_tool_route(test_config):

    for valid_id in test_config["online_tool_endpoint"]["valid_lpa_online_tool_ids"]:
        status, response = send_a_request(
            test_config=test_config,
            url=f"{test_config['online_tool_endpoint']['url']}/{valid_id}",
            method=test_config["online_tool_endpoint"]["method"],
        )

        assert status == 200
        response_dict = json.loads(response)
        assert response_dict["onlineLpaId"] == valid_id
        assert is_valid_schema(response_dict, "lpa_online_tool_schema.json")


@pytest.mark.parametrize("test_config", configs_to_test)
def test_online_tool_route_invalid_id(test_config):

    for valid_id in test_config["online_tool_endpoint"]["invalid_lpa_online_tool_ids"]:
        status, response = send_a_request(
            test_config=test_config,
            url=f"{test_config['online_tool_endpoint']['url']}/{valid_id}",
            method=test_config["online_tool_endpoint"]["method"],
        )

        assert status == 404
        response_dict = json.loads(response)
        assert response_dict == {}
