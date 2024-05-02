#!/usr/bin/env python3
import json
import connexion
from flask import Response, jsonify, request
import requests
import logging

from api.lpas.handlers import handle_lpa_get, handle_request_letter


def healthcheck():
    return "OK", 200


def getLpas(*args, **kwargs):
    status_code, response_message = handle_lpa_get(query_params=kwargs)
    logging.info(f"status_code: {status_code}")
    logging.info(f"response_message: {response_message}")

    return response_message, int(status_code)


def requestCode(request):
    status_code, response_message = handle_request_letter(
        caseUid=request.get('case_uid', None),
        actorUid=request.get('actor_uid', None),
        notes=request.get('notes', None)
    )
    logging.info(f"status_code: {status_code}")
    logging.info(f"response_message: {response_message}")

    return response_message, int(status_code)


def createOrder():
    return "Not implemented", 501


def createDeputyDocument():
    return "Not implemented", 501


def getDeputyDocuments():
    return "Not implemented", 501


def updateDeputyDocument():
    return "Not implemented", 501


def updateSendStatus():
    return "Not implemented", 501


logging.basicConfig(level=logging.INFO)
sirius_server = connexion.FlaskApp(__name__)
sirius_server.add_api("sirius_public_api.yaml")
sirius_server.add_api("sirius_secret_api.yaml")
sirius_server.run(port=5001)
