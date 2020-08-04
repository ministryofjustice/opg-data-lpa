from .api.resources import api as api_blueprint


def create_app(Flask):
    app = Flask(__name__)

    app.register_blueprint(api_blueprint)

    routes = [str(p) for p in app.url_map.iter_rules()]
    print(f"routes: {routes}")


    return app
