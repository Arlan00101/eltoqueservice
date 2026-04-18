from flask import Flask
from app.config import config


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from app.routes import api_bp

    app.register_blueprint(api_bp)

    return app
