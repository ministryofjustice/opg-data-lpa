import datetime
import os
from urllib.parse import urlparse, urlencode, quote

import boto3
import jwt
import localstack_client.session

import requests
from botocore.exceptions import ClientError


from .helpers import custom_logger

logger = custom_logger("sirius_service")


def build_sirius_url(endpoint, url_params=None):
    """
    Builds the url for the endpoint from variables (probably saved in env vars)

    Args:
        base_url: URL of the Sirius server
        api_route: path to public api
        endpoint: endpoint
    Returns:
        string: url
    """

    try:
        base_url = os.environ["SIRIUS_BASE_URL"]
    except KeyError as e:
        logger.error(f"Unable to build Sirius URL {e}")
        raise Exception

    sirius_url = f"{base_url}/{quote(endpoint)}"

    if url_params:
        encoded_params = urlencode(url_params)
        url = f"{sirius_url}?{encoded_params}"
    else:
        url = sirius_url

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

    try:
        if os.environ['ENVIRONMENT'] == 'local':
            current_session = localstack_client.session.Session()


        else:
            current_session = boto3.session.Session()
    except KeyError:
        current_session = boto3.session.Session()

    client = current_session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
    except ClientError as e:
        logger.info(f"Unable to get secret from Secrets Manager {e}")
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

    if not content_type:
        content_type = "application/json"

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


def handle_sirius_error(error_code=None, error_message=None, error_details=None):
    error_code = error_code if error_code else 500
    error_message = (
        error_message if error_message else "Unknown error talking to " "Sirius"
    )

    try:
        error_details = error_details["detail"]

    except (KeyError, TypeError):
        error_details = str(error_details) if len(str(error_details)) > 0 else "None"

    message = f"{error_message}, details: {str(error_details)}"
    logger.error(message)
    return error_code, message


def send_request_to_sirius(url, method, content_type=None, data=None):

    headers = build_sirius_headers(content_type)

    try:
        if method == "PUT":
            r = requests.put(url=url, data=data, headers=headers)
            return r.status_code, r.json()

        elif method == "POST":
            r = requests.post(url=url, data=data, headers=headers)
            return r.status_code, r.json()
        elif method == "GET":
            r = requests.get(url=url, headers=headers)
            return r.status_code, r.json()
        else:
            return handle_sirius_error(
                error_message=f"Unable to send request to Sirius",
                error_details=f"Method {method} not allowed on Sirius route",
            )

    except Exception as e:
        return handle_sirius_error(
            error_message=f"Unable to send request to Sirius", error_details=e
        )
