import pytest
import json
from .conftest import send_a_request, configs_to_test, is_valid_schema


@pytest.mark.smoke_test
@pytest.mark.parametrize("test_config", configs_to_test)
def test_healthcheck_route(test_config):

    if test_config["name"] == "original collections api on aws dev":
        print("Healthcheck does not exist on original collections api on aws dev")
        pass
    else:

        status, response = send_a_request(
            test_config=test_config,
            url=f"{test_config['healthcheck_endpoint']['url']}",
            method=test_config["healthcheck_endpoint"]["method"],
        )

        assert status == 200
        response_dict = json.loads(response)
        assert is_valid_schema(response_dict, "healthcheck_schema.json")
