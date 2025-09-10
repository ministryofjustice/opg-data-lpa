import fakeredis

from lambda_functions.v1.functions.lpa.opg_sirius_service.sirius_handler import SiriusService
from .default_config import SiriusServiceTestConfig


def test_check_cache_available():
    fake_redis_server = fakeredis.FakeServer()
    test_redis_handler = fakeredis.FakeStrictRedis(
        charset="utf-8", decode_responses=True, server=fake_redis_server
    )
    test_sirius_service = SiriusService(
        config_params=SiriusServiceTestConfig, cache=test_redis_handler
    )

    result = test_sirius_service.check_cache_available()

    assert result is True


def test_check_cache_not_available():
    fake_redis_server = fakeredis.FakeServer()
    fake_redis_server.connected = False
    test_redis_handler = fakeredis.FakeStrictRedis(
        charset="utf-8", decode_responses=True, server=fake_redis_server
    )
    test_sirius_service = SiriusService(
        config_params=SiriusServiceTestConfig, cache=test_redis_handler
    )

    result = test_sirius_service.check_cache_available()

    assert result is False
