import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.db import execute, fetch_one

app = create_app()

with app.app_context():
    malicious_input = "' OR '1'='1"

    try:
        execute(
            """
            INSERT INTO events (
                title,
                event_date,
                start_time,
                end_time
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                malicious_input,
                "2026-11-10",
                "10:00:00",
                "11:00:00"
            ),
            database=app.config["MYSQL_TEST_DATABASE"]
        )

        result = fetch_one(
            """
            SELECT title
            FROM events
            WHERE title = %s
            """,
            (malicious_input,),
            database=app.config["MYSQL_TEST_DATABASE"]
        )

        assert result is not None
        assert result["title"] == malicious_input

        print("GODKÄNT: Indata behandlas som vanlig text.")

    finally:
        execute(
            "DELETE FROM events WHERE title = %s",
            (malicious_input,),
            database=app.config["MYSQL_TEST_DATABASE"]
        )