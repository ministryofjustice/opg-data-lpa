import redis
from flask import Flask


from .api.resources import api as api_blueprint
from .api.sirius_service import SiriusService
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)

    app.config.from_object(config)

    app.register_blueprint(api_blueprint)

    app.redis = redis.StrictRedis.from_url(
        url=config.REDIS_URL, charset="utf-8", decode_responses=True
    )

    app.sirius = SiriusService(config_params=config, cache=app.redis)

    return app
