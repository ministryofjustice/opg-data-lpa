from flask import current_app
from werkzeug.exceptions import abort

from .helpers import custom_logger


from .sirius_helpers import (
    format_uid_response,
    format_online_tool_response,
    generate_sirius_url,
)

logger = custom_logger()


def get_by_online_tool_id(lpa_online_tool_id):

    sirius_url = generate_sirius_url(lpa_online_tool_id=lpa_online_tool_id)

    sirius_status_code, sirius_response = current_app.sirius.send_request_to_sirius(
        key=lpa_online_tool_id, url=sirius_url, method="GET"
    )

    if sirius_status_code in [200]:
        if len(sirius_response) > 0:
            try:
                return format_online_tool_response(sirius_response=sirius_response), 200
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

    sirius_status_code, sirius_response = current_app.sirius.send_request_to_sirius(
        key=sirius_uid, url=sirius_url, method="GET"
    )
    if sirius_status_code in [200]:
        if len(sirius_response) > 0:
            try:
                return format_uid_response(sirius_response=sirius_response), 200
            except Exception as e:
                logger.error(f"Error formatting sirius response: {e}")
                abort(404)
        else:
            logger.error(f"Sirius data empty")
            abort(404)
    else:
        logger.error(f"Sirius error: {sirius_status_code}")
        abort(404)


def get_service_status():

    sirius_status = (
        "OK" if current_app.sirius.check_sirius_available() is True else "Unavailable"
    )

    if current_app.sirius.cache is not None:
        cache_status = (
            "OK" if current_app.sirius.check_cache_available() else "Unavailable"
        )
    else:
        cache_status = "Not enabled"

    return {
        "data": {
            "api-status": "OK",
            "sirius-status": sirius_status,
            "cache-status": cache_status,
        },
        "meta": None,
    }
