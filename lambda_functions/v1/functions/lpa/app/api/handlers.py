import json
import os

import urllib3
from werkzeug.exceptions import abort

from .helpers import custom_logger

# from .sirius_service import build_sirius_url, send_request_to_sirius
from . import sirius_service

logger = custom_logger()


def get_by_online_tool_id(lpa_online_tool_id):

    sirius_url = generate_sirius_url(lpa_online_tool_id=lpa_online_tool_id)

    sirius_status_code, sirius_response = sirius_service.send_request_to_sirius(
        key=lpa_online_tool_id, url=sirius_url, method="GET"
    )

    if sirius_status_code in [200]:
        if len(sirius_response) > 0:
            try:
                return format_response(sirius_response=sirius_response), 200
            except Exception as e:
                logger.error(f"Error formatting sirius response: {e}")
                abort(404)
        else:
            logger.error(f"Sirius data empty")
            abort(404)
    else:
        logger.error(f"Sirius error: {sirius_status_code}")
        abort(404)


def get_by_sirius_uid(sirius_uid):
    sirius_url = generate_sirius_url(sirius_uid=sirius_uid)

    sirius_status_code, sirius_response = sirius_service.send_request_to_sirius(
        url=sirius_url, method="GET"
    )
    if sirius_status_code in [200]:
        if len(sirius_response) > 0:
            try:
                return sirius_response, 200
            except Exception as e:
                logger.error(f"Error formatting sirius response: {e}")
                abort(404)
        else:
            logger.error(f"Sirius data empty")
            abort(404)
    else:
        logger.error(f"Sirius error: {sirius_status_code}")
        abort(404)


def generate_sirius_url(lpa_online_tool_id=None, sirius_uid=None):
    sirius_api_version = os.environ["SIRIUS_API_VERSION"]
    sirius_api_url = f"api/public/{sirius_api_version}/lpas"
    if lpa_online_tool_id:
        sirius_url_params = {"lpa-online-tool-id": lpa_online_tool_id}
    elif sirius_uid:
        sirius_url_params = {"uid": sirius_uid}

    url = sirius_service.build_sirius_url(
        endpoint=sirius_api_url, url_params=sirius_url_params,
    )

    return url


def format_response(sirius_response):

    logger.info(f"type(sirius_response): {type(sirius_response)}")
    lpa_data = sirius_response[0]

    result = {
        "onlineLpaId": lpa_data["onlineLpaId"],
        "receiptDate": lpa_data["receiptDate"],
        "registrationDate": lpa_data["registrationDate"],
        "rejectedDate": lpa_data["rejectedDate"],
        "status": lpa_data["status"],
    }

    return result
