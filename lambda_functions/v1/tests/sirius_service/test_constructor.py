import json
import logging

import fakeredis
import pytest

from lambda_functions.v1.functions.lpa.app.api.sirius_service import SiriusService
from lambda_functions.v1.functions.lpa.app.config import LocalTestingConfig, Config


def test_constructor():
    test_redis_handler = fakeredis.FakeStrictRedis(
        charset="utf-8", decode_responses=True
    )
    test_sirius_service = SiriusService(
        config_params=LocalTestingConfig, cache=test_redis_handler
    )

    assert test_sirius_service.cache is not None
    assert test_sirius_service.sirius_base_url is not None
    assert test_sirius_service.environment is not None
    assert test_sirius_service.session_data is not None
    assert test_sirius_service.request_caching is not None
    assert test_sirius_service.request_caching_name is not None
    assert test_sirius_service.request_caching_ttl is not None


class BrokenConfig(Config):
    del Config.SIRIUS_BASE_URL


def test_constructor_broken(caplog):

    test_redis_handler = fakeredis.FakeStrictRedis(
        charset="utf-8", decode_responses=True
    )
    SiriusService(config_params=BrokenConfig, cache=test_redis_handler)

    with caplog.at_level("INFO"):
        assert "Error loading config" in caplog.text


class EmptyConfig(LocalTestingConfig):
    REQUEST_CACHE_NAME = None
    REQUEST_CACHING_TTL = None


def test_constructor_defaults():
    test_redis_handler = fakeredis.FakeStrictRedis(
        charset="utf-8", decode_responses=True
    )
    test_sirius_service = SiriusService(
        config_params=EmptyConfig, cache=test_redis_handler
    )

    assert test_sirius_service.request_caching_name == "default_sirius_cache"
    assert test_sirius_service.request_caching_ttl == 48


def test_constructor_redis_not_connected():

    test_sirius_service = SiriusService(config_params=LocalTestingConfig, cache=None)

    print(f"test_sirius_service: {test_sirius_service}")
    assert test_sirius_service.request_caching == "disabled"
