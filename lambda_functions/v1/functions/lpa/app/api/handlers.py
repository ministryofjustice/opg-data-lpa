from flask import current_app
from werkzeug.exceptions import abort

from .helpers import custom_logger, get_event_details_for_logs
import json
import traceback

from .sirius_helpers import (
    format_uid_response,
    format_online_tool_response,
    generate_sirius_url,
)

logger = custom_logger("handlers")


def get_by_online_tool_id(lpa_online_tool_id):
    sirius_url = generate_sirius_url(lpa_online_tool_id=lpa_online_tool_id)

    try:
        (
            sirius_status_code,
            sirius_response,
        ) = current_app.sirius.send_request_to_sirius(
            key=lpa_online_tool_id, url=sirius_url, method="GET"
        )
        use_cache = current_app.sirius.use_cache
    except Exception as e:
        stack_trace = traceback.format_exc()
        message = f"Internal server error: {e} --- {stack_trace}"
        logger.error(
            message,
            extra=get_event_details_for_logs(
                status=500, key=lpa_online_tool_id, cache_used=False
            ),
        )
        abort(500)

    if sirius_status_code in [200, 410]:
        if len(sirius_response) > 0:
            try:
                response = (
                    format_online_tool_response(sirius_response=sirius_response)
                    if sirius_status_code == 200
                    else ""
                )
                logger.info(
                    "Get By Online Tool Id - OK",
                    extra=get_event_details_for_logs(
                        status=sirius_status_code,
                        key=lpa_online_tool_id,
                        cache_used=use_cache,
                    ),
                )
                return response, sirius_status_code
            except Exception as e:
                logger.error(
                    f"Error formatting sirius response: {e}",
                    extra=get_event_details_for_logs(
                        status=sirius_status_code,
                        key=lpa_online_tool_id,
                        cache_used=use_cache,
                    ),
                )
                abort(404)
        else:
            logger.error(
                f"Sirius data empty",
                extra=get_event_details_for_logs(
                    status=sirius_status_code,
                    key=lpa_online_tool_id,
                    cache_used=use_cache,
                ),
            )
            abort(404)
    else:
        logger.error(
            f"Sirius error: {sirius_status_code}",
            extra=get_event_details_for_logs(
                status=sirius_status_code, key=lpa_online_tool_id, cache_used=use_cache
            ),
        )
        abort(404)


def get_by_sirius_uid(sirius_uid):
    sirius_url = generate_sirius_url(sirius_uid=sirius_uid)

    try:
        (
            sirius_status_code,
            sirius_response,
        ) = current_app.sirius.send_request_to_sirius(
            key=sirius_uid, url=sirius_url, method="GET"
        )
        use_cache = current_app.sirius.use_cache
    except Exception as e:
        stack_trace = traceback.format_exc()
        logger.error(
            f"Internal server error: {e} --- {stack_trace}",
            extra=get_event_details_for_logs(
                status=500, key=sirius_uid, cache_used=False
            ),
        )
        abort(500)
    if sirius_status_code in [200, 410]:
        if len(sirius_response) > 0:
            try:
                response = (
                    format_uid_response(sirius_response=sirius_response)
                    if sirius_status_code == 200
                    else sirius_response[0]
                )

                logger.info(
                    "Get By Sirius UID - OK",
                    extra=get_event_details_for_logs(
                        status=sirius_status_code, key=sirius_uid, cache_used=use_cache
                    ),
                )

                return response, sirius_status_code
            except Exception as e:
                logger.error(
                    f"Error formatting sirius response: {e}",
                    extra=get_event_details_for_logs(
                        status=sirius_status_code, key=sirius_uid, cache_used=use_cache
                    ),
                )
                abort(404)
        else:
            logger.error(
                f"Sirius data empty",
                extra=get_event_details_for_logs(
                    status=sirius_status_code, key=sirius_uid, cache_used=use_cache
                ),
            )
            abort(404)
    else:
        logger.error(
            f"Sirius error: {sirius_status_code}",
            extra=get_event_details_for_logs(
                status=sirius_status_code, key=sirius_uid, cache_used=use_cache
            ),
        )
        abort(404)


def request_code(body):
    sirius_url = current_app.sirius.build_sirius_url(
        endpoint="api/public/v1/lpas/requestCode"
    )
    try:
        sirius_status_code, sirius_response = current_app.sirius.send_request_to_sirius(
            key=None,
            url=sirius_url,
            method="POST",
            data=json.dumps(body) if isinstance(body, dict) else body,
        )
    except Exception as e:
        stack_trace = traceback.format_exc()
        logger.error(
            f"Internal server error contacting Sirius: {e} --- {stack_trace}",
            extra=get_event_details_for_logs(
                status=500, key=str(body), cache_used=False
            ),
        )
        abort(500)
    if sirius_status_code != 204 and sirius_status_code != 200:
        logger.error(
            f"Sirius error: {sirius_status_code}",
            extra=get_event_details_for_logs(
                status=sirius_status_code, key=str(body), cache_used=False
            ),
        )
    else:
        logger.info(
            "Post Request Code - OK",
            extra=get_event_details_for_logs(
                status=sirius_status_code, key=str(body), cache_used=False
            ),
        )
    return sirius_response, sirius_status_code


def get_service_status():
    sirius_status = (
        "OK" if current_app.sirius.check_sirius_available() is True else "Unavailable"
    )

    if current_app.sirius.request_caching == "enabled":
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
