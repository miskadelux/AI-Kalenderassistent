import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.db import get_db_connection

app = create_app()

with app.app_context():
    connection = None

    try:
        with get_db_connection(
            database=app.config["MYSQL_TEST_DATABASE"]
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            raise RuntimeError("Simulerat fel")

    except RuntimeError:
        print("Simulerat fel fångat.")

    assert not connection.open, "Databasanslutningen stängdes inte!"

    print("GODKÄNT: Databasanslutningen stängdes efter felet.")