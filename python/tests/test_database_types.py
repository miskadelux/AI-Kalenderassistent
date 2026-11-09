import sys
from datetime import date, datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.db import fetch_one

app = create_app()

with app.app_context():
    result = fetch_one(
        """
        SELECT event_date, start_time, created_at
        FROM events
        LIMIT 1
        """,
        database=app.config["MYSQL_TEST_DATABASE"]
    )

    assert result is not None, "Inga testposter hittades."

    assert isinstance(result["event_date"], date)
    assert isinstance(result["start_time"], timedelta)
    assert isinstance(result["created_at"], datetime)

    print("GODKÄNT: Alla datatyper är korrekta.")

    for column, value in result.items():
        print(f"{column}: {value}")
        print(f"Python-typ: {type(value).__name__}")
        print("---")