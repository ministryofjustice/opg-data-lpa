import urllib3

from .sirius_service import build_sirius_url


def get_by_online_tool_id(lpa_online_tool_id):

    sirius_url = generate_sirius_url(lpa_online_tool_id=lpa_online_tool_id)

    response_message = {"message": f"OK {lpa_online_tool_id}", "sirius_url": sirius_url}
    print(f"message: {response_message}")

    return response_message, 200


def get_by_sirius_uid(sirius_uid):

    sirius_url = generate_sirius_url(sirius_uid=sirius_uid)

    response_message = {"message": f"OK {sirius_uid}", "sirius_url": sirius_url}
    print(f"message: {response_message}")

    return response_message, 200


def generate_sirius_url(lpa_online_tool_id=None, sirius_uid=None):
    sirius_base_url = "https://fake_url.com"
    sirius_api_version = "v1"
    sirius_api_url = "api/public/lpas"
    if lpa_online_tool_id:
        sirius_url_params = {"lpa-online-tool-id": lpa_online_tool_id}
    elif sirius_uid:
        sirius_url_params = {"id": sirius_uid}

    url = build_sirius_url(
        base_url=sirius_base_url,
        version=sirius_api_version,
        endpoint=sirius_api_url,
        url_params=sirius_url_params,
    )

    return url
