import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_secretsmanager

from lambda_functions.v1.functions.lpa.app.api import sirius_service


@pytest.mark.parametrize(
    "secret_code, environment, region",
    [("i_am_a_secret_code", "development", "eu-west-1")],
)
@mock_secretsmanager
def test_get_secret(secret_code, environment, region):

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)

    client.create_secret(Name=f"{environment}/jwt-key", SecretString=secret_code)
    assert sirius_service.get_secret(environment) == secret_code

    with pytest.raises(ClientError):
        sirius_service.get_secret("not_a_real_environment")
