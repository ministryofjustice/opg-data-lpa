import pytest
import json
from .conftest import send_a_request, configs_to_test, is_valid_schema


@pytest.mark.smoke_test
@pytest.mark.parametrize("test_config", configs_to_test)
def test_request_code_route(test_config):

    for valid_id in test_config["request_code_endpoint"]["valid_sirius_uids"]:
        status, response = send_a_request(
            test_config=test_config,
            url=f"{test_config['request_code_endpoint']['url']}",
            method=test_config["request_code_endpoint"]["method"],
            payload={"case_uid": int(valid_id), "actor_uid": 70005}
        )

        assert status == 204