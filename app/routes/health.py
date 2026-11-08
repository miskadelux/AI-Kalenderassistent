import time

import requests
from flask import Blueprint, current_app, jsonify

from app.db import check_database

health_bp = Blueprint("health", __name__)


def check_ollama():
    """
    Kontrollerar Ollama och att konfigurerad modell finns installerad.
    """
    start_time = time.perf_counter()
    timeout = current_app.config["HEALTH_CHECK_TIMEOUT"]

    try:
        host = current_app.config["OLLAMA_HOST"].rstrip("/")
        model = current_app.config["OLLAMA_MODEL"]

        response = requests.get(
            f"{host}/api/tags",
            timeout=timeout
        )

        response.raise_for_status()

        models = response.json().get("models", [])

        installed_models = {
            item.get("name", "").removesuffix(":latest")
            for item in models
        }

        expected_model = model.removesuffix(":latest")

        model_exists = expected_model in installed_models

        status = "reachable" if model_exists else "model_missing"

    except requests.RequestException:
        status = "unreachable"

    except (ValueError, TypeError, AttributeError):
        status = "unreachable"

    response_time = round(
        (time.perf_counter() - start_time) * 1000, 2
    )

    return {
        "status": status,
        "response_time_ms": response_time
    }


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Kontrollerar databas och Ollama och returnerar applikationens hälsostatus.
    """
    mysql = check_database()
    ollama = check_ollama()

    mysql_ok = mysql["status"] == "connected"
    ollama_ok = ollama["status"] == "reachable"

    if mysql_ok and ollama_ok:
        overall_status = "healthy"
    elif mysql_ok and ollama["status"] == "model_missing" or mysql_ok or ollama_ok:
        overall_status = "degraded"
    else:
        overall_status = "unhealthy"

    response = {
        "status": overall_status,
        "components": {
            "mysql": mysql,
            "ollama": ollama
        }
    }

    http_status = 200 if overall_status == "healthy" else 503

    return jsonify(response), http_status
