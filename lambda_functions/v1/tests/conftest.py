import pytest
import os

from lambda_functions.v1.functions.lpa.app import api


@pytest.fixture(autouse=True)
def aws_credentials(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-west-1")
    monkeypatch.setenv("AWS_XRAY_CONTEXT_MISSING", "LOG_ERROR")
    monkeypatch.setenv("SIRIUS_BASE_URL", "http://not-really-sirius.com")
    monkeypatch.setenv("SIRIUS_API_VERSION", "v1")
    monkeypatch.setenv("SESSION_DATA", "publicapi@opgtest.com")
    monkeypatch.setenv("ENVIRONMENT", "not-a-real-environment")
    monkeypatch.setenv("JWT_SECRET", "THIS_IS_MY_SECRET_KEY")
