import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.db import fetch_all
from app.serializers import serialize_data

app = create_app()

with app.app_context():
    results = fetch_all(
        """
        SELECT event_date, start_time, created_at
        FROM events
        """,
        database=app.config["MYSQL_TEST_DATABASE"]
    )

    serialized = serialize_data(results)

    json_output = json.dumps(
    serialized,
    ensure_ascii=False,
    indent=4
    )

    assert isinstance(json.loads(json_output), list)

    print("GODKÄNT: JSON-serialisering fungerar.")
    print(json_output)