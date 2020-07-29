import os

from flask import Blueprint, abort
from flask import request, jsonify

from .errors import error_message
from .helpers import custom_logger
from .endpoints import handle_template

logger = custom_logger("template")

version = os.getenv("API_VERSION")
api = Blueprint("api", __name__, url_prefix=f"/{version}")


@api.app_errorhandler(404)
def handle404(error=None):
    return error_message(404, "Not found url {}".format(request.url))


@api.app_errorhandler(405)
def handle405(error=None):
    return error_message(405, "Method not supported")


@api.app_errorhandler(400)
def handle400(error=None):
    return error_message(400, "Bad payload")


@api.app_errorhandler(500)
def handle500(error=None):
    return error_message(500, f"Something went wrong: {error}")


@api.route("/healthcheck", methods=["HEAD", "GET"])
def handle_healthcheck():
    response_message = "OK"

    return jsonify(response_message), 200


@api.route("/example_route", methods=["GET"])
def template_route():
    """
    Add purpose of this route here.

    Add Additional info here.

    Returns:
        Add what is returned here
    """

    result, status_code = handle_template()

    return jsonify(result), status_code
