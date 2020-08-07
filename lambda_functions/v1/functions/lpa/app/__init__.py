from flask import Flask

from .api.resources import api as api_blueprint
from .api.sirius_service import SiriusService
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)

    app.config.from_object(config)

    app.register_blueprint(api_blueprint)

    app.sirius = SiriusService(config_params=config)

    return app
