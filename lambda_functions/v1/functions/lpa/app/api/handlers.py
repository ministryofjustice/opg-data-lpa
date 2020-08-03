import json
import os

import urllib3

from .sirius_service import build_sirius_url, send_request_to_sirius


def get_by_online_tool_id(lpa_online_tool_id):
    sirius_url = generate_sirius_url(lpa_online_tool_id=lpa_online_tool_id)

    sirius_status_code, sirius_response = send_request_to_sirius(
        url=sirius_url, method="GET"
    )
    print(f"sirius_response: {sirius_response}")

    response_message = (format_response(sirius_response=sirius_response),)
    print(f"response_message: {response_message}")

    return response_message, 200


def get_by_sirius_uid(sirius_uid):
    sirius_url = generate_sirius_url(sirius_uid=sirius_uid)

    sirius_status_code, sirius_response = send_request_to_sirius(
        url=sirius_url, method="GET"
    )

    response_message = sirius_response

    return response_message, 200


def generate_sirius_url(lpa_online_tool_id=None, sirius_uid=None):
    sirius_api_version = os.environ["SIRIUS_API_VERSION"]
    sirius_api_url = f"api/public/{sirius_api_version}/lpas"
    if lpa_online_tool_id:
        sirius_url_params = {"lpa-online-tool-id": lpa_online_tool_id}
    elif sirius_uid:
        sirius_url_params = {"uid": sirius_uid}

    url = build_sirius_url(endpoint=sirius_api_url, url_params=sirius_url_params,)

    return url


def format_response(sirius_response):

    lpa_data = sirius_response

    result = {
        "onlineLpaId": lpa_data["onlineLpaId"],
        "receiptDate": lpa_data["receiptDate"],
        "registrationDate": lpa_data["registrationDate"],
        "rejectedDate": lpa_data["rejectedDate"],
        "status": lpa_data["status"],
    }

    return result
