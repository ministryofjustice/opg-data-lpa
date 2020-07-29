import datetime
import os
from urllib.parse import urlparse, urlencode

import boto3
import jwt
from botocore.exceptions import ClientError

from .helpers import custom_logger

logger = custom_logger("sirius_service")


def build_sirius_url(base_url, version, endpoint, url_params=None):
    """
    Builds the url for the endpoint from variables (probably saved in env vars)

    Args:
        base_url: URL of the Sirius server
        api_route: path to public api
        endpoint: endpoint
    Returns:
        string: url
    """

    url_parts = [base_url, version, endpoint]

    sirius_url = "/".join([i for i in url_parts if i is not None])

    if url_params:
        encoded_params = urlencode(url_params)
        url = f"{sirius_url}?{encoded_params}"
    else:
        url = sirius_url

    if urlparse(url).scheme not in ["https", "http"]:
        logger.info("Unable to build Sirius URL")
        raise Exception

    return url


def get_secret(environment):
    """
    Gets and decrypts the JWT secret from AWS Secrets Manager for the chosen environment
    This was c&p directly from AWS Secrets Manager...

    Args:
        environment: AWS environment name
    Returns:
        JWT secret
    Raises:
        ClientError
    """

    secret_name = f"{environment}/jwt-key"
    region_name = "eu-west-1"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
    except ClientError as e:
        logger.info("Unable to get secret from Secrets Manager")
        raise e

    return secret


def build_sirius_headers(content_type="application/json"):
    """
    Builds headers for Sirius request, including JWT auth

    Args:
        content_type: string, defaults to 'application/json'
    Returns:
        Header dictionary with content type and auth token
    """
    environment = os.environ["ENVIRONMENT"]
    session_data = os.environ["SESSION_DATA"]

    encoded_jwt = jwt.encode(
        {
            "session-data": session_data,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3600),
        },
        get_secret(environment),
        algorithm="HS256",
    )

    return {
        "Content-Type": content_type,
        "Authorization": "Bearer " + encoded_jwt.decode("UTF8"),
    }
