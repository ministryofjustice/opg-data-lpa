from flask import Flask

from .functions.lpa.app import create_app
from .config import LocalMockConfig

lambda_handler = create_app(flask=Flask, config=LocalMockConfig)
