import json

import fakeredis

from lambda_functions.v1.functions.lpa.app.opg_sirius_service.sirius_handler import (
    SiriusService,
)
from .conftest import test_sirius_service
from .default_config import SiriusServiceTestConfig

test_cache = test_sirius_service.cache


def test_put_sirius_data_in_cache():

    test_sirius_service.request_caching_name = "my_cache"
    test_sirius_service.request_caching_ttl = 20

    test_sirius_service._put_sirius_data_in_cache(
        key="lpa_1234", data={"caseType": "pfa"}, status=200
    )

    full_key = "my_cache-lpa_1234-200"

    assert test_cache.get(full_key) == '{"caseType": "pfa"}'
    assert test_cache.ttl(full_key) == 20 * 60 * 60

    test_cache.flushall()


def test_put_sirius_data_in_cache_broken(caplog):

    test_key = "test_key"
    test_data = {"test": "data"}

    fake_redis_server = fakeredis.FakeServer()
    fake_redis_server.connected = False
    test_redis_handler = fakeredis.FakeStrictRedis(
        charset="utf-8", decode_responses=True, server=fake_redis_server
    )
    test_sirius_service = SiriusService(
        config_params=SiriusServiceTestConfig, cache=test_redis_handler
    )

    test_sirius_service._put_sirius_data_in_cache(
        key=test_key, data=json.dumps(test_data), status="fail"
    )

    with caplog.at_level("ERROR"):
        assert "Unable to set cache" in caplog.text
