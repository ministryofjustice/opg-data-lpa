#!/usr/bin/env python3
import json
import connexion
from flask import Response, jsonify, request
import requests
import logging

from api.lpas.handlers import handle_lpa_get


def getLpas(*args, **kwargs):

    status_code, response_message = handle_lpa_get(query_params=kwargs)
    logging.info(f"status_code: {status_code}")
    logging.info(f"response_message: {response_message}")

    return response_message, int(status_code)


logging.basicConfig(level=logging.INFO)
sirius_server = connexion.FlaskApp(__name__)
sirius_server.add_api("sirius_public_api.yaml")
sirius_server.run(port=5001)
