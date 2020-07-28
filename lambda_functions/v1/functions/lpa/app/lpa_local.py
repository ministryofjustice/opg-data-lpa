from . import create_app
from flask import Flask

lambda_handler = create_app(Flask)

routes = [str(p) for p in lambda_handler.url_map.iter_rules()]
print(f"routes: {routes}")
