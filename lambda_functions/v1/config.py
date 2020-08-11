from .functions.lpa.app import Config


class LocalMockConfig(Config):
    # override prod values
    DEBUG = True
    TESTING = True
    LOGGER_LEVEL = "DEBUG"

    REQUEST_CACHING = "enabled"
    REQUEST_CACHE_NAME = "opg-data-lpa-local"

    # specific to local testing
    HYPOTHESIS_MAX_EXAMPLES = 50
    LOCALSTACK_HOST = "motoserver"
    JWT_SECRET = "THIS_IS_MY_SECRET_KEY"  # pragma: allowlist secret


class LocalTestingConfig(Config):
    # override prod values
    DEBUG = True
    TESTING = True
    LOGGER_LEVEL = "DEBUG"

    SIRIUS_BASE_URL = "http://not-really-sirius.com"
    SESSION_DATA = "publicapi@opgtest.com"

    REQUEST_CACHING = "enabled"
    REQUEST_CACHING_TTL = 48
    REQUEST_CACHE_NAME = "opg-data-lpa-local"
    REDIS_URL = "redis://redis:6379"

    # specific to local testing
    HYPOTHESIS_MAX_EXAMPLES = 50
    LOCALSTACK_HOST = "motoserver"
    JWT_SECRET = "THIS_IS_MY_SECRET_KEY"  # pragma: allowlist secret
