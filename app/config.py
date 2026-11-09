
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    MYSQL_HOST = os.getenv("DB_HOST")
    MYSQL_USER = os.getenv("DB_USER")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
    MYSQL_DATABASE = os.getenv("DB_NAME")
    MYSQL_TEST_DATABASE = os.getenv("DB_TEST_NAME")

    OLLAMA_HOST = os.getenv("OLLAMA_HOST")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    HEALTH_CHECK_TIMEOUT = 3
    DB_CONNECT_TIMEOUT = 5

    @classmethod
    def validate(cls):
        required_variables = [
            "DB_HOST",
            "DB_USER",
            "DB_PASSWORD",
            "DB_NAME",
            "DB_TEST_NAME",
            "OLLAMA_HOST",
            "OLLAMA_MODEL",
        ]

        missing = [
            variable
            for variable in required_variables
            if not os.getenv(variable)
        ]

        if missing:
            raise RuntimeError(
                "Saknar obligatoriska miljövariabler: "
                + ", ".join(missing)
            )
