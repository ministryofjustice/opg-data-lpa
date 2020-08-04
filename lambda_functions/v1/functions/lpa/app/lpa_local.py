
from . import create_app
from flask import Flask

lambda_handler = create_app(Flask)


