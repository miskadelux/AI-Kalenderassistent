import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

try:
    print("ansluter till databasen som användare", db_user)

    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 AS test_val;")
        result = cursor.fetchone()
        print(f"Koplingen lyckades! Testfrågan gav SVAR: ", result)

        cursor.execute("SELECT COUNT(*) AS event_count FROM events;")
        count_result = cursor.fetchone()
        num_events = count_result['event_count']
        print(f"Antal rader i events-tabellen: {num_events}")

except pymysql.MySQLError as e:
    print(f"\n[FEL] Kunde inte ansluta till databasen. Konteollera att MySQL är igång och att uppgifterna i .env stämmer.")
    print(SystemError(f"Tekniskt felmedelande: {e}"))

finally:
    if "connection" in locals() and connection.open:
        connection.close()
        print("Databasanslutningen stängdes säkert.")
