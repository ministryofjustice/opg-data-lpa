import datetime
import json
from urllib.parse import urlencode, quote

import boto3
import jwt
import localstack_client.session
import requests
from botocore.exceptions import ClientError

import logging

logger = logging


class SiriusService:
    def __init__(self, config_params, cache):
        try:
            self.cache = cache
            self.use_cache = False
            self.sirius_base_url = config_params.SIRIUS_BASE_URL
            self.environment = config_params.ENVIRONMENT
            self.session_data = config_params.SESSION_DATA
            self.request_timeout = config_params.REQUEST_TIMEOUT
            self.request_caching = (
                config_params.REQUEST_CACHING if cache else "disabled"
            )
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
            raise Exception(f"Error loading config e: {e}")

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
            logger.debug("Using local AWS Secrets Manager")  # pragma: no cover
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
            raise Exception(f"Unable to get secret from Secrets Manager: {e}")

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
            "Authorization": "Bearer " + encoded_jwt,
        }

    def _handle_sirius_error(
        self, error_code=None, error_message=None, error_details=None
    ):
        error_code = error_code if error_code else 500
        error_message = (
            error_message if error_message else "Unknown error talking to Sirius"
        )

        try:
            error_details = error_details["detail"]

        except (KeyError, TypeError):
            error_details = (
                str(error_details) if len(str(error_details)) > 0 else "None"
            )

        message = f"{error_message}, details: {str(error_details)}"
        return error_code, message

    def check_sirius_available(self):
        healthcheck_url = f"{self.sirius_base_url}/api/health-check"
        try:
            return (
                True
                if requests.get(
                    url=healthcheck_url, timeout=self.request_timeout
                ).status_code
                == 200
                else False
            )
        except Exception as e:
            logger.error(f"Sirius Unavailable: {e}")
            return False

    def check_cache_available(self):
        try:
            return self.cache.ping()
        except Exception as e:
            logger.error(f"Unable to connect to cache: {e}")
            return False

    def send_request_to_sirius(self, key, url, method, content_type=None, data=None):
        cache_enabled = True if self.request_caching == "enabled" else False
        self.use_cache = False
        if self.check_sirius_available():
            sirius_status_code, sirius_data = self._get_data_from_sirius(
                url, method, content_type, data
            )
            logger.debug(f"sirius_status_code: {sirius_status_code}")
            logger.debug(f"cache_enabled: {cache_enabled}")
            logger.debug(f"method: {method}")
            if cache_enabled and method == "GET":
                if sirius_status_code == 200 or sirius_status_code == 410:
                    logger.debug(f"Putting data in cache with key: {key}")
                    self._put_sirius_data_in_cache(
                        key=key, data=sirius_data, status=sirius_status_code
                    )

            return sirius_status_code, sirius_data
        else:
            if cache_enabled and method == "GET":
                self.use_cache = True
                logger.debug(f"Getting data from cache with key: {key}")
                sirius_status_code, sirius_data = self._get_sirius_data_from_cache(
                    key=key
                )

                return sirius_status_code, sirius_data
            else:
                sirius_status_code, sirius_data = self._handle_sirius_error(
                    error_message="Unable to send request to Sirius",
                    error_details="Sirius not available - cache not enabled or incorrect method for cache",
                )
                return sirius_status_code, sirius_data

    def _get_data_from_sirius(self, url, method, content_type=None, data=None):
        logger.debug("_get_data_from_sirius")
        headers = self._build_sirius_headers(content_type)

        try:
            if method == "PUT":
                r = requests.put(url=url, data=data, headers=headers)
                return r.status_code, r.json()

            elif method == "POST":
                r = requests.post(url=url, data=data, headers=headers)
                if r.status_code == 204:
                    return r.status_code, ""

                return r.status_code, r.json()
            elif method == "GET":
                r = requests.get(url=url, headers=headers, timeout=self.request_timeout)
                return r.status_code, r.json()
            else:
                return self._handle_sirius_error(
                    error_message="Unable to send request to Sirius",
                    error_details=f"Method {method} not allowed on Sirius route",
                )

        except Exception as e:
            return self._handle_sirius_error(
                error_message="Unable to send request to Sirius", error_details=e
            )

    def _put_sirius_data_in_cache(self, key, data, status):
        logger.debug("_put_sirius_data_in_cache")
        cache_name = self.request_caching_name
        cache_ref = f"{cache_name}-{key}"

        cache_ttl_in_seconds = self.request_caching_ttl * 60 * 60

        data = json.dumps(data)

        try:
            self.cache.set(
                name=f"{cache_ref}-{status}", value=data, ex=cache_ttl_in_seconds
            )
            logger.debug(f"setting redis: {cache_ref}-{status}")
        except Exception as e:
            logger.error(f"Unable to set cache: {cache_ref}-{status}, error {e}")

    def _get_sirius_data_from_cache(self, key):
        cache_name = self.request_caching_name
        cache_ref = f"{cache_name}-{key}"

        try:
            if self.cache.exists(f"{cache_ref}-200"):
                logger.debug(f"found redis cache: {cache_ref}-200")
                status_code = 200
                result = self.cache.get(f"{cache_ref}-200")
                result = json.loads(result)
            elif self.cache.exists(f"{cache_ref}-410"):
                logger.debug(f"found redis cache: {cache_ref}-410")
                status_code = 410
                result = self.cache.get(f"{cache_ref}-410")
                result = json.loads(result)
            else:
                logger.debug(f"no-cache exists for: {cache_ref}-[200, 410]")
                status_code = 500
                result = None
        except Exception as e:
            logger.error(f"Unable to get from cache: {cache_ref}, error {e}")
            status_code = 500
            result = None

        return status_code, result
