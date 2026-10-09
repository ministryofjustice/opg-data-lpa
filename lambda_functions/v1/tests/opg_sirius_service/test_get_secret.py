import boto3
import pytest
from botocore.stub import Stubber
from moto import mock_aws

from .conftest import test_sirius_service


@pytest.mark.parametrize(
    "secret_code, environment, region",
    [("i_am_a_secret_code", "not_a_real_env", "eu-west-1")],
)
@mock_aws
def test_get_secret(secret_code, environment, region):
    client = boto3.client("secretsmanager")
    stubber = Stubber(client)

    stubber.add_response(
        "get_secret_value",
        {"SecretString": secret_code},
        {"SecretId": f"{environment}/jwt-key"},
    )
    stubber.activate()

    test_sirius_service.secretsmanager = client
    test_sirius_service.environment = environment
    assert test_sirius_service._get_secret() == secret_code

    with pytest.raises(Exception):
        test_sirius_service.environment = "not_the_right_env"
        test_sirius_service._get_secret()
