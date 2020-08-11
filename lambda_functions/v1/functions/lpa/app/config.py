import os


class Config(object):
    DEBUG = False
    TESTING = False
    LOGGER_LEVEL = "INFO"
    API_VERSION = "v1"
    API_NAME = "opg-data-lpa"
    ENVIRONMENT = os.environ.get("ENVIRONMENT")

    # sirius
    SIRIUS_BASE_URL = os.environ.get("SIRIUS_BASE_URL")
    SESSION_DATA = os.environ.get("SESSION_DATA")

    # caching
    REQUEST_CACHE_NAME = API_NAME
    REQUEST_CACHING_TTL = 48

    REDIS_URL = os.environ.get("REDIS_URL")
    REQUEST_CACHING = os.environ.get("REQUEST_CACHING", default="disabled")
