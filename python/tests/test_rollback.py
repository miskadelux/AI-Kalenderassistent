import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.db import fetch_one, get_db_connection

app = create_app()

with app.app_context():
    try:
        with get_db_connection(
            database=app.config["MYSQL_TEST_DATABASE"]
        ) as connection, connection.cursor() as cursor:
            cursor.execute(
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
                    "Rollback-test",
                    "2026-11-10",
                    "10:00:00",
                    "11:00:00"
                )
            )

            raise RuntimeError("Simulerat fel")

    except RuntimeError:
        print("Simulerat fel fångat.")

    result = fetch_one(
        """
        SELECT id
        FROM events
        WHERE title = %s
        """,
        ("Rollback-test",),
        database=app.config["MYSQL_TEST_DATABASE"]
    )
    assert result is None, "Rollback misslyckades: dataposten finns kvar."

    print("GODKÄNT: Transaktionen återställdes.")