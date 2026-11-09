import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.db import DatabaseError, execute

app = create_app()

with app.app_context():
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
                "Ogiltig sluttid-test",
                "2026-11-10",
                "11:00:00",
                "10:00:00"
            ),
            database=app.config["MYSQL_TEST_DATABASE"]
        )

    except DatabaseError as error:
        if error.error_code == 3819:
            print("GODKÄNT: CHECK-villkoret blockerade ogiltig sluttid.")
        else:
            raise

    else:
        execute(
            "DELETE FROM events WHERE title = %s",
            ("Ogiltig sluttid-test",),
            database=app.config["MYSQL_TEST_DATABASE"]
        )
        raise AssertionError("CHECK-villkoret blockerade inte ogiltig sluttid.")