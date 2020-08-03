import json
import os
from os.path import join, dirname

import boto3
import requests
from boto3.session import Session
from jsonschema import validate, exceptions
from requests_aws4auth import AWS4Auth

opg_sirius_api_gateway_dev_aws = {
    "name": "original collections api on aws dev",
    "online_tool_endpoint": {
        "url": "https://3d9iqi6bq9.execute-api.eu-west-1.amazonaws.com/v1/lpa-online-tool/lpas",
        "method": "GET",
        "valid_lpa_online_tool_ids": ["A33718377316"],
        "invalid_lpa_online_tool_ids": ["banana"],
    },
    "use_an_lpa_endpoint": {
        "url": "https://3d9iqi6bq9.execute-api.eu-west-1.amazonaws.com/v1/use-an-lpa/lpas",
        "method": "GET",
        "valid_sirius_uids": ["700000000013"],
        "invalid_sirius_uids": ["9"],
    },
}


opg_data_lpa_dev_aws = {
    "name": "new collections api on aws dev",
    "online_tool_endpoint": {
        "url": "https://in316.dev.lpa.api.opg.service.justice.gov.uk/v1/lpa-online-tool/lpas",
        "method": "GET",
        "valid_lpa_online_tool_ids": ["A33718377316"],
        "invalid_lpa_online_tool_ids": ["banana"],
    },
    "use_an_lpa_endpoint": {
        "url": "https://in316.dev.lpa.api.opg.service.justice.gov.uk/v1/use-an-lpa/lpas",
        "method": "GET",
        "valid_sirius_uids": ["700000000013"],
        "invalid_sirius_uids": ["9"],
    },
}

configs_to_test = [opg_data_lpa_dev_aws]


def pytest_html_report_title(report):
    report.title = "opg-data-lpa integration tests"


def send_a_request(
    test_config,
    url=None,
    method=None,
    payload=None,
    extra_headers=None,
    content_type=None,
):
    print(f"Using test_config: {test_config['name']}")

    headers = {
        "Content-Type": content_type if content_type else "application/json",
    }

    if extra_headers:
        for h in extra_headers:
            headers[h["header_name"]] = h["header_value"]

    if payload:
        body = json.dumps(payload)
    else:
        body = None

    if "CI" in os.environ:
        role_name = "sirius-ci"
    else:
        role_name = "operator"

    boto3.setup_default_session(region_name="eu-west-1",)

    client = boto3.client("sts")
    client.get_caller_identity()["Account"]

    role_to_assume = f"arn:aws:iam::288342028542:role/{role_name}"

    response = client.assume_role(
        RoleArn=role_to_assume, RoleSessionName="assumed_role"
    )

    session = Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
    )

    client = session.client("sts")
    client.get_caller_identity()["Account"]

    credentials = session.get_credentials()

    credentials = credentials.get_frozen_credentials()
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    token = credentials.token

    auth = AWS4Auth(
        access_key, secret_key, "eu-west-1", "execute-api", session_token=token,
    )

    response = requests.request(method, url, auth=auth, data=body, headers=headers)

    print(f"response.status_code: {response.status_code}")
    print(f"response: {json.dumps(response.json(), indent=4)}")

    return response.status_code, response.text


def is_valid_schema(data, schema_file):
    """ Checks whether the given data matches the schema """
    schema = load_data(schema_file, as_json=False)
    try:
        validate(data, schema)
        result = True
    except exceptions.ValidationError as e:
        print("well-formed but invalid JSON:", e)
        result = False
    except json.decoder.JSONDecodeError as e:
        print("poorly-formed text, not JSON:", e)
        result = False

    return result


def load_data(filename, as_json=True):
    relative_path = join("response_schemas", filename)
    absolute_path = join(dirname(__file__), relative_path)

    with open(absolute_path) as data_file:
        if as_json:
            return data_file.read()
        else:
            return json.loads(data_file.read())
