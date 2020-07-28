import pytest

from pact_provider.check_pact_deployable import PactDeploymentCheck

import boto3
from moto import mock_secretsmanager, mock_sts


@pytest.mark.parametrize(
    "secret_code, environment, region",
    [("i_am_a_secret_code", "development", "eu-west-1")],
)
@pytest.mark.pact_test
@mock_secretsmanager
@mock_sts
def test_get_secret(secret_code, environment, region):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)

    client.create_secret(Name="pactbroker_admin", SecretString=secret_code)

    assert PactDeploymentCheck.get_secret("pactbroker_admin") == secret_code
    assert PactDeploymentCheck.get_secret("local") == "dummy_password"
