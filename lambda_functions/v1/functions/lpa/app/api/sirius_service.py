import datetime
import json
from urllib.parse import urlencode, quote

import boto3
import jwt
import localstack_client.session
import requests
from botocore.exceptions import ClientError

from .helpers import custom_logger

logger = custom_logger("sirius_service")


class SiriusService:
    def __init__(self, config_params, cache):

        try:
            self.cache = cache
            self.sirius_base_url = config_params.SIRIUS_BASE_URL
            self.environment = config_params.ENVIRONMENT
            self.session_data = config_params.SESSION_DATA
            self.redis_url = config_params.REDIS_URL
            self.request_caching = config_params.REQUEST_CACHING
            self.request_caching_name = (
                config_params.REQUEST_CACHE_NAME
                if config_params.REQUEST_CACHE_NAME
                else "default_sirius_cache"
            )
            self.request_caching_ttl = (
                config_params.REQUEST_CACHING_TTL
                if config_params.REQUEST_CACHING_TTL
                else 48
            )
        except Exception as e:
            logger.info(f"Error loading config e: {e}")

    def build_sirius_url(self, endpoint, url_params=None):
        """
        Builds the url for the endpoint from variables (probably saved in env vars)

        Args:
            base_url: URL of the Sirius server
            api_route: path to public api
            endpoint: endpoint
        Returns:
            string: url
        """

        base_url = self.sirius_base_url

        sirius_url = f"{base_url}/{quote(endpoint)}"

        if url_params:
            encoded_params = urlencode(url_params)
            url = f"{sirius_url}?{encoded_params}"
        else:
            url = sirius_url

        return url

    def _get_secret(self):
        """
        Gets and decrypts the JWT secret from AWS Secrets Manager for the chosen environment
        This was c&p directly from AWS Secrets Manager...

        Args:
            environment: AWS environment name
        Returns:
            JWT secret
        Raises:
            ClientError
        """

        environment = self.environment
        secret_name = f"{environment}/jwt-key"
        region_name = "eu-west-1"

        if environment == "local":  # pragma: no cover
            logger.info("Using local AWS Secrets Manager")  # pragma: no cover
            current_session = localstack_client.session.Session()  # pragma: no cover

        else:
            current_session = boto3.session.Session()

        client = current_session.client(
            service_name="secretsmanager", region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            secret = get_secret_value_response["SecretString"]
        except ClientError as e:
            logger.info(f"Unable to get secret from Secrets Manager {e}")
            raise e

        return secret

    def _build_sirius_headers(self, content_type="application/json"):
        """
        Builds headers for Sirius request, including JWT auth

        Args:
            content_type: string, defaults to 'application/json'
        Returns:
            Header dictionary with content type and auth token
        """

        if not content_type:
            content_type = "application/json"

        session_data = self.session_data

        encoded_jwt = jwt.encode(
            {
                "session-data": session_data,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3600),
            },
            self._get_secret(),
            algorithm="HS256",
        )

        return {
            "Content-Type": content_type,
            "Authorization": "Bearer " + encoded_jwt.decode("UTF8"),
        }

    def _handle_sirius_error(
        self, error_code=None, error_message=None, error_details=None
    ):
        error_code = error_code if error_code else 500
        error_message = (
            error_message if error_message else "Unknown error talking to " "Sirius"
        )

        try:
            error_details = error_details["detail"]

        except (KeyError, TypeError):
            error_details = (
                str(error_details) if len(str(error_details)) > 0 else "None"
            )

        message = f"{error_message}, details: {str(error_details)}"
        logger.error(message)
        return error_code, message

    def _check_sirius_available(self):
        healthcheck_url = f"{self.sirius_base_url}/health-check"
        r = requests.get(url=healthcheck_url)

        return True if r.status_code == 200 else False
        # return True

    def send_request_to_sirius(self, key, url, method, content_type=None, data=None):

        cache_enabled = True if self.request_caching == "enabled" else False

        redis_service = self.cache

        if self._check_sirius_available():
            sirius_status_code, sirius_data = self._get_data_from_sirius(
                url, method, content_type, data
            )
            logger.info(f"sirius_status_code: {sirius_status_code}")
            logger.info(f"cache_enables: {cache_enabled}")
            logger.info(f"method: {method}")
            if cache_enabled and method == "GET" and sirius_status_code == 200:
                logger.info(f"Putting data in cache with key: {key}")
                self._put_sirius_data_in_cache(
                    redis_conn=redis_service, key=key, data=sirius_data
                )

            return sirius_status_code, sirius_data
        else:
            if cache_enabled and method == "GET":
                logger.info(f"Getting data from cache with key: {key}")
                sirius_status_code, sirius_data = self._get_sirius_data_from_cache(
                    redis_conn=redis_service, key=key
                )

                return sirius_status_code, sirius_data
            else:
                return self._handle_sirius_error(
                    error_message=f"Unable to send request to Sirius",
                    error_details=f"Sirius not available",
                )

    def _get_data_from_sirius(self, url, method, content_type=None, data=None):

        headers = self._build_sirius_headers(content_type)

        try:
            if method == "PUT":
                r = requests.put(url=url, data=data, headers=headers)
                return r.status_code, r.json()

            elif method == "POST":
                r = requests.post(url=url, data=data, headers=headers)
                return r.status_code, r.json()
            elif method == "GET":
                r = requests.get(url=url, headers=headers)

                return r.status_code, r.json()
            else:
                return self._handle_sirius_error(
                    error_message=f"Unable to send request to Sirius",
                    error_details=f"Method {method} not allowed on Sirius route",
                )

        except Exception as e:
            return self._handle_sirius_error(
                error_message=f"Unable to send request to Sirius", error_details=e
            )

    def _put_sirius_data_in_cache(self, redis_conn, key, data):
        cache_name = self.request_caching_name

        cache_ttl_in_seconds = self.request_caching_ttl * 60 * 60

        data = json.dumps(data)

        redis_conn.set(name=f"{cache_name}-{key}", value=data, ex=cache_ttl_in_seconds)

        logger.info(f"setting redis: {cache_name}-{key}")

    def _get_sirius_data_from_cache(self, redis_conn, key):

        cache_name = (
            self.request_caching_name
            if self.request_caching_name
            else self.default_caching_name
        )

        logger.info(f"getting redis: {cache_name}-{key}")
        logger.info(
            f'redis_conn.exists(f"{cache_name}-{key}"): {redis_conn.exists(f"{cache_name}-{key}")}'
        )

        if redis_conn.exists(f"{cache_name}-{key}"):
            status_code = 200
            result = redis_conn.get(f"{cache_name}-{key}")
            result = json.loads(result)
        else:
            status_code = 500
            result = None

        return status_code, result
