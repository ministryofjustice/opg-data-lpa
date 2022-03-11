import os

from flask import Blueprint
from flask import request, jsonify

from .errors import error_message
from .handlers import get_by_online_tool_id, get_by_sirius_uid, get_service_status, request_code
from .helpers import custom_logger


logger = custom_logger("")

version = "v1"
print(f"version: {version}")
api = Blueprint("api", __name__, url_prefix=f"/{version}")

# TODO Not sure how many of these are actually implemented, and some will get caught
#  at the gateway. Needs a tidy up, but right now it's like the so it reflects the spec


@api.app_errorhandler(400)
def handle400(error=None):
    return error_message(400, "Bad request")


@api.app_errorhandler(403)
def handle403(error=None):
    return error_message(400, "Authentication failed")


@api.app_errorhandler(404)
def handle404(error=None):
    return error_message(404, "An LPA with the passed ID Not Found")


@api.app_errorhandler(405)
def handle405(error=None):
    return error_message(405, "Method not supported")


@api.app_errorhandler(410)
def handle410(error=None):
    return error_message(410, "An LPA with the passed ID has been deleted from The Sirius data provider")


@api.app_errorhandler(429)
def handle429(error=None):
    return error_message(405, "API Gateway throttling limit exceeded")


@api.app_errorhandler(500)
def handle500(error=None):
    return error_message(500, f"Something went wrong: {error}")


@api.app_errorhandler(502)
def handle502(error=None):
    return error_message(500, "Unhandled internal exception within OPG Gateway")


@api.app_errorhandler(504)
def handle504(error=None):
    return error_message(500, "The Sirius data provider timed out")


@api.route("/healthcheck", methods=["HEAD", "GET"])
def handle_healthcheck_route():
    response_message = get_service_status()

    return jsonify(response_message), 200


@api.route("/lpa-online-tool/lpas/<lpa_online_tool_id>", methods=["GET"])
def handle_lpa_online_tool(lpa_online_tool_id):
    logger.info(f"lpa_online_tool_id: {lpa_online_tool_id}")

    response, status = get_by_online_tool_id(lpa_online_tool_id=lpa_online_tool_id)

    return jsonify(response), status


@api.route("/use-an-lpa/lpas/<sirius_uid>", methods=["GET"])
def handle_use_an_lpa(sirius_uid):
    logger.info(f"sirius_uid: {sirius_uid}")

    response, status = get_by_sirius_uid(sirius_uid=sirius_uid)

    return jsonify(response), status


@api.route("/use-an-lpa/lpas/requestCode", methods=["POST"])
def handle_request_code():
    body = request.json
    logger.info(f"body: {body}")

    response, status = request_code(body)

    return jsonify(response), status
