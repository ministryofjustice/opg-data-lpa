import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_secretsmanager

from lambda_functions.v1.tests.sirius_service.conftest import test_sirius_service


@pytest.mark.parametrize(
    "secret_code, environment, region",
    [("i_am_a_secret_code", "development", "eu-west-1")],
)
@mock_secretsmanager
def test_get_secret(secret_code, environment, region):

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)

    client.create_secret(Name=f"{environment}/jwt-key", SecretString=secret_code)

    test_sirius_service.environment = environment
    assert test_sirius_service._get_secret() == secret_code

    with pytest.raises(ClientError):
        test_sirius_service.environment = "not_a_real_env"
        test_sirius_service._get_secret()
