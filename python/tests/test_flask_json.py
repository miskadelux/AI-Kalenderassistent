import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from flask import jsonify

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
    response = jsonify(serialized)

    json_data = json.loads(response.get_data(as_text=True))

    assert isinstance(json_data, list)

    if json_data:
        assert isinstance(json_data[0]["event_date"], str)
        assert isinstance(json_data[0]["start_time"], str)
        assert isinstance(json_data[0]["created_at"], str)

    print("GODKÄNT: Flask JSON-konvertering fungerar.")
    print(response.get_data(as_text=True))