from flask import current_app

from lambda_functions.v1.functions.lpa.app.api.helpers import custom_logger

logger = custom_logger()


def generate_sirius_url(lpa_online_tool_id=None, sirius_uid=None):
    sirius_api_version = "v1"
    sirius_api_url = f"api/public/{sirius_api_version}/lpas"
    if lpa_online_tool_id:
        sirius_url_params = {"lpa-online-tool-id": lpa_online_tool_id}
    elif sirius_uid:
        sirius_url_params = {"uid": sirius_uid}

    logger.info(f"sirius_api_url: {sirius_api_url}")

    url = current_app.sirius.build_sirius_url(
        endpoint=sirius_api_url, url_params=sirius_url_params,
    )

    return url


def format_uid_response(sirius_response):
    return sirius_response[0]


def format_online_tool_response(sirius_response):

    lpa_data = sirius_response[0]

    result = {
        "onlineLpaId": lpa_data["onlineLpaId"],
        "receiptDate": lpa_data["receiptDate"],
        "registrationDate": lpa_data["registrationDate"],
        "rejectedDate": lpa_data["rejectedDate"],
        "status": lpa_data["status"],
    }

    return result
