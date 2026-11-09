import logging
import time
from contextlib import contextmanager

import pymysql
from flask import current_app
from pymysql.constants import CLIENT

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Eget undantag för databasrelaterade fel."""

    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code


def check_database():
    """
    Kontrollerar databasanslutningen.
    Returnerar en säker felstatus utan att exponera känslig information.
    """
    start_time = time.perf_counter()
    timeout = current_app.config["HEALTH_CHECK_TIMEOUT"]

    try:
        with get_db_connection(timeout=timeout) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        status = "connected"

    except DatabaseError as error:
        if error.error_code in (1045, 1698):
            status = "authentication_failed"
        elif error.error_code == 1044:
            status = "database_access_denied"
        elif error.error_code == 1049:
            status = "database_not_found"
        elif error.error_code in (2002, 2003, 2006, 2013):
            status = "server_unavailable"
        else:
            status = "connection_failed"

    except TimeoutError:
        status = "timeout"

    response_time = round(
        (time.perf_counter() - start_time) * 1000, 2
    )

    return {
        "status": status,
        "response_time_ms": response_time
    }


@contextmanager
def get_db_connection(timeout=None, database=None):
    """
    Skapar och hanterar en MySQL-anslutning.

    Commits vid lyckad operation, gör rollback vid fel
    och stänger alltid anslutningen.

    Args:
        timeout: Valfri timeout i sekunder.
        database: Valfri databas som ska användas.

    Yields:
        pymysql.connections.Connection: Aktiv databasanslutning.

    Raises:
        DatabaseError: Om en databasoperation misslyckas.
    """
    if timeout is None:
        timeout = current_app.config.get("DB_CONNECT_TIMEOUT")

    if database is None:
        database = current_app.config["MYSQL_DATABASE"]

    connection = None

    try:
        connection = pymysql.connect(
            host=current_app.config["MYSQL_HOST"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=timeout,
            read_timeout=timeout,
            write_timeout=timeout,
            autocommit=False,
            client_flag=CLIENT.FOUND_ROWS
        )

        yield connection

        connection.commit()

    except pymysql.MySQLError as error:
        if connection is not None:
            try:
                connection.rollback()
            except pymysql.MySQLError:
                logger.exception("Databasens rollback misslyckades.")

        error_code = error.args[0] if error.args else None

        logger.exception("Ett databasfel inträffade.")

        raise DatabaseError(
            "Databasoperationen misslyckades.",
            error_code=error_code
        ) from error

    except Exception:
        if connection is not None:
            try:
                connection.rollback()
            except pymysql.MySQLError:
                logger.exception("Databasens rollback misslyckades.")

        raise

    finally:
        if connection is not None:
            try:
                connection.close()
            except pymysql.MySQLError:
                logger.exception("Kunde inte stänga databasanslutningen.")


def fetch_all(sql, params=None, database=None):
    """
    Hämtar samtliga rader från en SQL-fråga.

    Args:
        sql: SQL-frågan med %s som platshållare.
        params: Parametrar till SQL-frågan.
        database: Valfri databas som ska användas.

    Returns:
        list[dict]: Samtliga matchande rader.

    Raises:
        DatabaseError: Om databasfrågan misslyckas.
    """
    with get_db_connection(database=database) as connection, connection.cursor() as cursor:
        cursor.execute(sql, params or ())
        return cursor.fetchall()


def fetch_one(sql, params=None, database=None):
    """
    Hämtar en rad från en SQL-fråga.

    Args:
        sql: SQL-frågan med %s som platshållare.
        params: Parametrar till SQL-frågan.
        database: Valfri databas som ska användas.

    Returns:
        dict | None: Den matchande raden eller None.

    Raises:
        DatabaseError: Om databasfrågan misslyckas.
    """
    with get_db_connection(database=database) as connection, connection.cursor() as cursor:
        cursor.execute(sql, params or ())
        return cursor.fetchone()


def execute(sql, params=None, database=None):
    """
    Kör en SQL-operation som ändrar data.

    Args:
        sql: SQL-frågan med %s som platshållare.
        params: Parametrar till SQL-frågan.
        database: Valfri databas som ska användas.

    Returns:
        dict: Innehåller lastrowid och rowcount.

    Raises:
        DatabaseError: Om databasoperationen misslyckas.
    """
    with get_db_connection(database=database) as connection, connection.cursor() as cursor:
        cursor.execute(sql, params or ())

        return {
            "lastrowid": cursor.lastrowid,
            "rowcount": cursor.rowcount
        }
