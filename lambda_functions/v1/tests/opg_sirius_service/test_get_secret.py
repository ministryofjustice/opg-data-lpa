import boto3
import pytest
from moto import mock_aws

from .conftest import test_sirius_service


@pytest.mark.parametrize(
    "secret_code, environment, region",
    [("i_am_a_secret_code", "not_a_real_env", "eu-west-1")],
)
@mock_aws
def test_get_secret(secret_code, environment, region):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)

    client.create_secret(Name=f"{environment}/jwt-key", SecretString=secret_code)
    test_sirius_service.environment = environment
    assert test_sirius_service._get_secret() == secret_code

    with pytest.raises(Exception):
        test_sirius_service.environment = "not_the_right_env"
        test_sirius_service._get_secret()
