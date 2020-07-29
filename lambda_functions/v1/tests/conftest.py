import pytest
import os


@pytest.fixture(autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"  # pragma: allowlist secret
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
    os.environ["AWS_XRAY_CONTEXT_MISSING"] = "LOG_ERROR"
    os.environ["SIRIUS_BASE_URL"] = "http://not-really-sirius.com"
    os.environ["SIRIUS_API_VERSION"] = "v1"
    os.environ["SESSION_DATA"] = "publicapi@opgtest.com"
    os.environ["JWT_SECRET"] = "THIS_IS_MY_SECRET_KEY"  # pragma: allowlist secret
