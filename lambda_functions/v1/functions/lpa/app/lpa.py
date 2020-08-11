from .flask_lambda import FlaskLambda
from . import create_app
from .config import ProductionConfig

lambda_handler = create_app(flask=FlaskLambda, config=ProductionConfig)
