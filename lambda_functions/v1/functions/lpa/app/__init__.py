import redis
from flask import Flask


from .api.resources import api as api_blueprint

from opg_sirius_service.sirius_handler import SiriusService
from .config import Config


def create_app(flask=Flask, config=Config):
    app = flask(__name__)

    app.config.from_object(config)

    app.register_blueprint(api_blueprint)

    if config.REQUEST_CACHING == "enabled":
        app.redis = redis.StrictRedis.from_url(
            url=f"redis://{config.REDIS_URL}", encoding="utf-8", decode_responses=True
        )

        redis_cache = app.redis

    else:
        redis_cache = None

    app.sirius = SiriusService(config_params=config, cache=redis_cache)

    return app
