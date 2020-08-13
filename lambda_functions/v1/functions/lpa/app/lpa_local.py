from . import create_app
from flask import Flask

from .config import LocalMockConfig

lambda_handler = create_app(flask=Flask, config=LocalMockConfig)
