import pytest
import json
from .conftest import send_a_request, configs_to_test, is_valid_schema


@pytest.mark.smoke_test
@pytest.mark.parametrize("test_config", configs_to_test)
def test_request_code_route(test_config):
    for lpa in test_config["request_code_endpoint"]["valid_sirius_lpas"]:
        status, response = send_a_request(
            test_config=test_config,
            url=f"{test_config['request_code_endpoint']['url']}",
            method=test_config["request_code_endpoint"]["method"],
            payload={"case_uid": lpa["caseUid"], "actor_uid": lpa["actorUid"]},
        )

        assert status == 204
