import pytest
import json
from .conftest import send_a_request, configs_to_test, is_valid_schema


@pytest.mark.smoke_test
@pytest.mark.parametrize("test_config", configs_to_test)
def test_use_an_lpa_route(test_config):
    for valid_id in test_config["use_an_lpa_endpoint"]["valid_sirius_uids"]:
        status, response = send_a_request(
            test_config=test_config,
            url=f"{test_config['use_an_lpa_endpoint']['url']}/{valid_id}",
            method=test_config["use_an_lpa_endpoint"]["method"],
        )

        assert status == 200
        response_dict = json.loads(response)
        # TODO we are getting a list from sirius?
        assert is_valid_schema(response_dict, "use_an_lpa_schema.json")
        assert response_dict["uId"].replace("-", "") == valid_id


@pytest.mark.smoke_test
@pytest.mark.parametrize("test_config", configs_to_test)
def test_use_an_lpa_route_invalid_id(test_config):
    for valid_id in test_config["use_an_lpa_endpoint"]["invalid_sirius_uids"]:
        status, response = send_a_request(
            test_config=test_config,
            url=f"{test_config['use_an_lpa_endpoint']['url']}/{valid_id}",
            method=test_config["use_an_lpa_endpoint"]["method"],
        )

        assert status == 404
