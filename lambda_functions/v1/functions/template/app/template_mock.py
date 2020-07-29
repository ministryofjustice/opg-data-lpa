import connexion
import json
from flask import Response
from connexion.exceptions import OAuthProblem


TOKEN_DB = {"asdf1234567890": {"uid": 100}}


def apikey_auth(token, required_scopes):
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem("Invalid token")

    return info


def get_invalid_response():
    validation_message = {
        "code": "OPGDATA-API-INVALIDREQUEST",
        "message": "Invalid Request",
    }
    response = Response(
        json.dumps(validation_message),
        status=400,
        mimetype="application/vnd.opg-data.v1+json",
    )
    return response


def rewrite_bad_request(response):
    if response.status_code == 400:
        validation_message = {
            "errors": [
                {"code": "OPGDATA-API-INVALIDREQUEST", "message": "Invalid Request"},
            ]
        }

        response = Response(
            json.dumps(validation_message),
            status=400,
            mimetype="application/vnd.opg-data.v1+json",
        )
    return response


mock = connexion.FlaskApp(__name__, specification_dir="../../../openapi/")
mock.app.after_request(rewrite_bad_request)
mock.add_api("template-openapi.yml", strict_validation="true")
mock.add_api("state-openapi.yml")
mock.run(port=4343)
