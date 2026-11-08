
from flask import Flask

from app.config import Config
from app.routes.health import health_bp


def create_app():
    Config.validate()

    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(health_bp)

    @app.route("/")
    def index():
        return {"message": "AI-kalenderassistent API"}

    return app
