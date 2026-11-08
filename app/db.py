
import time

import pymysql
from flask import current_app


def check_database():
    """
    Kontrollerar databasanslutningen.
    Returnerar en säker felstatus utan att exponera känslig information.
    """
    start_time = time.perf_counter()
    timeout = current_app.config["HEALTH_CHECK_TIMEOUT"]
    connection = None

    try:
        connection = pymysql.connect(
            host=current_app.config["MYSQL_HOST"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DATABASE"],
            connect_timeout=timeout,
            read_timeout=timeout,
            write_timeout=timeout
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        status = "connected"

    except pymysql.MySQLError as error:
        error_code = error.args[0] if error.args else None

        if error_code in (1045, 1698):
            status = "authentication_failed"
        elif error_code == 1044:
            status = "database_access_denied"
        elif error_code == 1049:
            status = "database_not_found"
        elif error_code in (2002, 2003, 2006, 2013):
            status = "server_unavailable"
        else:
            status = "connection_failed"

    except TimeoutError:
        status = "timeout"

    finally:
        if connection is not None:
            try:
                connection.close()
            except pymysql.MySQLError:
                pass

    response_time = round(
        (time.perf_counter() - start_time) * 1000, 2
    )

    return {
        "status": status,
        "response_time_ms": response_time
    }
