import logging

from flask import Blueprint, jsonify, request

from app.db import DatabaseError, fetch_all, fetch_one
from app.serializers import serialize_data
from app.validators import validate_date, validate_date_range

logger = logging.getLogger(__name__)

events_bp = Blueprint(
    "events",
    __name__,
    url_prefix="/events"
)


@events_bp.route("", methods=["GET"])
def get_events():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    try:
        if start_date is not None:
            start_date = validate_date(start_date, "start_date")

        if end_date is not None:
            end_date = validate_date(end_date, "end_date")

        validate_date_range(start_date, end_date)

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    sql = """
        SELECT *
        FROM events
    """

    conditions = []
    params = []

    if start_date is not None:
        conditions.append("event_date >= %s")
        params.append(start_date)

    if end_date is not None:
        conditions.append("event_date <= %s")
        params.append(end_date)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += """
        ORDER BY event_date ASC, start_time ASC, id ASC
    """

    try:
        events = fetch_all(sql, params)
        return jsonify(serialize_data(events)), 200

    except DatabaseError:
        logger.exception("Kunde inte hämta händelser.")
        return jsonify({"error": "Databasen är tillfälligt otillgänglig."}), 503





@events_bp.route("/<int:event_id>", methods=["GET"])
def get_event(event_id):
    sql = """
        SELECT *
        FROM events
        WHERE id = %s
    """

    try:
        event = fetch_one(sql, (event_id,))

        if event is None:
            return jsonify({"error": "Händelsen hittades inte."}), 404

        return jsonify(serialize_data(event)), 200

    except DatabaseError:
        logger.exception("Kunde inte hämta händelse med ID %s.", event_id)
        return jsonify({"error": "Databasen är tillfälligt otillgänglig."}), 503