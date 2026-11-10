
from flask import Flask, jsonify

from app.config import Config
from app.routes.events import events_bp
from app.routes.health import health_bp


def create_app():
    Config.validate()

    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(health_bp)
    app.register_blueprint(events_bp)

    @app.route("/")
    def index():
        return {"message": "AI-kalenderassistent API"}

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Resursen hittades inte."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "HTTP-metoden stöds inte."
        }), 405

    return app